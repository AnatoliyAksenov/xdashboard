<template>
   <md-content>
    <div class="md-layout md-gutter">
      <div class="md-layout-item md-small-size-100" style="width: 300px">
        <md-field>
          <label for="inn">ИНН</label>
          <md-input name="inn" id="inn" v-model="form.inn" />
        </md-field>
        <md-field>
          <label for="name">Наименование</label>
          <md-input name="name" id="name" v-model="form.name" />
        </md-field>
        <md-field>
          <label for="idx">idx</label>
          <md-input name="idx" id="idx" v-model="form.idx" />
        </md-field>
        <md-field>
          <label for="src">src</label>
          <md-input name="src" id="src" v-model="link.src" />
        </md-field>
        <md-field>
          <label for="trg">trg</label>
          <md-input name="trg" id="trg" v-model="link.trg" />
        </md-field>        
        <md-field>
          <md-button class="md-default" @click="addFromForm();">Add</md-button>
        </md-field>
      </div>
      <div class="md-layout-item">
        <div ref="graph"></div>
      </div>
    </div>
  </md-content>
</template>

<script>
  export default {
    props: [
      'inn',
      'date',
      'summ'
      ],    
    name: 'TransactionGraph',
    data: () => ({    
      data: [{'idx': '112233', "inn": '1111111111', 'name': 'X Company 1'}, {'idx': '332211', "inn": '2222222222', 'name': 'X Company 2'}],
      links: [{'src': "112233", 'trg': '332211'}],
      form: {},
      link: {},
    }),
    methods: {
      addNode(node){
        //TODO: Add checks
        this.data.push(node);
      },
      addLink(link){
        //TODO: Add checks
        this.links.push(link);
      },
      addFromForm(){
        
        this.data.push(this.form);
        this.form = {};

        this.links.push(this.link);
        this.link = {};
      }

    },
    mounted(){
      const width = 1200;
      const height = 800;

      const node_width = 300;

      const n = `
      <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="259" height="370" viewBox="-0.5 -0.5 259 370" style="background-color: rgb(255, 255, 255);">
        <defs>
          <filter id="dropShadow">
            <feGaussianBlur in="SourceAlpha" stdDeviation="1.7" result="blur"/>
            <feOffset in="blur" dx="3" dy="3" result="offsetBlur"/>
            <feFlood flood-color="#3D4574" flood-opacity="0.4" result="offsetColor"/>
            <feComposite in="offsetColor" in2="offsetBlur" operator="in" result="offsetBlur"/>
            <feBlend in="SourceGraphic" in2="offsetBlur"/>
          </filter>
        </defs>
        <g filter="url(#dropShadow)">
          <rect x="0" y="0" width="250" height="360" fill="#000000" stroke="#000000" pointer-events="all" transform="translate(2,3)" opacity="0.25"/>
          <rect x="0" y="0" width="250" height="360" fill="#ffffff" stroke="#eeeeee" pointer-events="all"/>
          <rect class="header" x="0" y="0" width="250" height="60" fill="none" stroke="none" pointer-events="all"  style="cursor: grab"/>
          <g fill="#000000" font-family="Helvetica" font-weight="bold" font-size="21px">
            <text x="15.5" y="39">7701998823</text>
          </g>
          <rect x="0" y="88" width="250" height="30" fill="none" stroke="none" pointer-events="none"/>
          <g fill="#808080" font-family="Helvetica" font-size="13px">
            <text x="17.5" y="112.5">Name</text>
          </g>
          <rect x="0" y="115" width="250" height="30" fill="none" stroke="none" pointer-events="none"/>
          <g fill="#000000" font-family="Helvetica" font-size="16px">
            <text x="17.5" y="136.5">X company name</text>
          </g>
          
          <path d="M 11.55 150 L 238.43 150" fill="none" stroke="#eeeeee" stroke-miterlimit="10" pointer-events="none"/>
          
          <rect x="0" y="300" width="90" height="60" fill="none" stroke="none" pointer-events="none"/>
          
          <g class="button" fill="#138FF2" font-family="Helvetica" font-weight="bold" text-anchor="middle" font-size="13px">
            <text x="44.5" y="335">REMOVE</text>
          </g>
          
          <rect x="160" y="300" width="90" height="60" fill="none" stroke="none" pointer-events="none"/>
          
          <g class="button" fill="#138FF2" font-family="Helvetica" font-weight="bold" text-anchor="middle" font-size="13px">
            <text x="204.5" y="335">ADD</text>
          </g>
        </g>
      </svg>
      `;

      const defs = `
      <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5"
        markerWidth="4" markerHeight="4"
        orient="auto">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#aaa" stroke="black" />
      </marker>
      <marker id="dot" viewBox="0 0 14 14" refX="5" refY="5"
        markerWidth="4" markerHeight="2">
        <circle cx="7" cy="7" r="7" fill="#aaa"/>
      </marker>
      `;

      const svg = d3.select(this.$refs.graph).append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("id", "main");
      
      svg.append('defs').html(defs);

      const g = svg.append("g");  
      const gl = svg.append("g");

      var zoom = d3.zoom()
        .extent([[0, 0], [width, height]])
        .scaleExtent([-2, 8])
        .on("zoom", zoomed)

      svg.call( zoom )
          .call(zoom.transform, d3.zoomIdentity);

      function zoomed(){
        let transform_offset = d3.event.transform;
        transform = transform_offset;

        g.attr("transform", d3.event.transform);
        d3.selectAll('path.link').attr("d", linkBuilder);

      }  


      // store mouse start position in current element
      var dx = 0;
      var dy = 0;
      var transform = {x: 0, y: 0, k: 1};

      function dragstarted() {
        const xo = d3.mouse(this);

        // save start mouse position in global vars 
        dx = xo[0];
        dy = xo[1];
        d3.select(this).attr("cursor", "grabbing");
      }

      function dragged(d) {
          // drag nodes
          const evt = d3.event;
          
          // use start mouse position for correcting event position
          d3.select(this).attr("transform",`translate(${evt.x - dx},${evt.y - dy})`); // parentElement - if had been used wrapper

          d3.selectAll('path.link').attr("d", linkBuilder);

      }

      function dragended() {
          d3.select(this).attr("cursor", "grab");
      }

      const linkVertical = d3.linkVertical()
          .source(d => d.src)
          .target(d => d.trg)
          .x(function(d) { return d.x; })
          .y(function(d) { return d.y; });


      const linkHorizontal = d3.linkHorizontal()
          .source(d => d.src)
          .target(d => d.trg)
          .x(function(d) { return d.x; })
          .y(function(d) { return d.y; });

      const linkData = (src, trg) => {
        // calc dots
        const dots =  [src, trg].reduce((r, e) => [...r, {
            0: { x: e.x + e.width / 2 , y: e.y },
            1: { x: e.x + e.width, y: e.y + e.height / 2 },
            2: { x: e.x + e.width / 2 , y: e.y + e.height },
            3: { x: e.x, y: e.y + e.height / 2 }
        }], [])

        // distance matrix
        const matrix = Object.keys(dots[0]).reduce((r, e) => [...r, Object.keys(dots[1]).reduce((rr, ee) => [...rr, ((dots[0][e].x - dots[1][ee].x) ** 2 + (dots[0][e].y - dots[1][ee].y) ** 2) ** 1 / 2], [])], []);

        // get the dots with the shortest distance 
        let m = matrix[0][0]
        let shortest = []
        for (let r in matrix) {
            for (let c in matrix[r]) {
                if (matrix[r][c] < m) {
                    shortest = [r, c];
                    m = matrix[r][c];
                }
            }
        }

        const link_type = shortest[0] % 2 == 0? 'V': 'H';
        const s = dots[0][ shortest[0] ];
        const t = dots[1][ shortest[1] ];

        return {"link_type": link_type, "src": s, "trg": t };
      }    

      const linkHovecal = (d) => {
        const src = d3.select(`g.nodes[idx="${d.src}"]`).node().getBBox(); //x, y, width, height
        const src_tr = d3.select(`g.nodes[idx="${d.src}"]`).node().getCTM()

        const trg = d3.select(`g.nodes[idx="${d.trg}"]`).node().getBBox();
        const trg_tr = d3.select(`g.nodes[idx="${d.trg}"]`).node().getCTM();
        
        const src_data = { x: src_tr.e + src.x * src_tr.a, y: src_tr.f + src.y * src_tr.d, width: src.width * transform.k, height: src.height * transform.k};
        const trg_data = { x: trg_tr.e + trg.x * trg_tr.a, y: trg_tr.f + trg.y * trg_tr.d, width: trg.width * transform.k, height: trg.height * transform.k};

        const link = linkData(src_data, trg_data);

        const params = {src: link.src, trg: link.trg};
        
        switch (link.link_type) {
            case 'V':
                return linkVertical(params);

            case 'H':
                return linkHorizontal(params);

        }
      }

      const linkBuilder = linkHovecal;

      const nodes = g.selectAll("g.nodes")
        .data( this.data )
        .join("g")
        .attr('class', 'nodes')
        .attr('transform', (d, i) => `translate(${ d.x ? d.x: node_width * i }, ${ d.y ? d.y: 10*i })`)
        .attr('idx', d => d.idx )
        .attr("x", (d, i) => ( d.x ? d.x: node_width * i) )
        .attr("y", (d, i) => (d.y ? d.y: 10*i) );


      const ui = nodes.selectAll('g.node')
        .data(d => [d])
        .join('g')
        .attr('class', 'node')
        .html(n)
        .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

      ui.select('.button')
        .call(d3.drag()
          .on("start", d => { if (d3.event.defaultPrevented) return; })
          .on("drag", d => { if (d3.event.defaultPrevented) return; })
          .on("end", d => { if (d3.event.defaultPrevented) return; }));


      const linkg = gl.selectAll("g.link")
        .data( this.links )
        .join("g")
        .attr("class", "link");

      linkg.selectAll('path.link')
        .data(d => [d])
        .join('path')
        .attr('class', 'link')
        .attr("src", d => d.src)
        .attr("trgt", d => d.trg)
        .attr("d", linkBuilder)
        .attr("idx", d => 'path_' + d.src + '_' + d.trg )
        .attr('class', "link");                
           

    }
  }
</script>

<style>
path.link {
    stroke: #aaa;
    stroke-width: 2px;
    stroke-linejoin: round;
    stroke-linecap: round;
    marker-start: url(#dot);
    marker-end: url(#arrow2);
    pointer-events: auto;
    fill: none;
}
</style>