<template>
	<div ref="chart"></div>
</template>

<script>
    import * as d3 from 'd3';
    window.d3 = d3;


	export default {
        props: [
            'data',
            'param',
            'idname'
        ],
        data: () => ({
            colorschema: "schemePastel1",
            decode: [],
            _current: null
        }),
        mounted(){

            var categorical = {
                "schemeAccent": d3.schemeAccent,
                "schemeDark2": d3.schemeDark2,
                "schemePastel2": d3.schemePastel2,
                "schemeSet2": d3.schemeSet2,
                "schemeSet1": d3.schemeSet1,
                "schemePastel1": d3.schemePastel1,
                "schemeCategory10": d3.schemeCategory10,
                "schemeSet3": d3.schemeSet3,
                "schemePaired": d3.schemePaired,
                //"schemeCategory20": d3.schemeCategory20,
                //"schemeCategory20b": d3.schemeCategory20b,
                //"schemeCategory20c": d3.schemeCategory20c
            };
            var width = 350;
            var height = 180;
            var opacity = .8;
            
            var radius = 80;
            var scheme = categorical[this.colorchema];
    
    // if(!window.pie_shared_color)
    //   window.pie_shared_color = d3.scaleOrdinal(scheme || d3.schemePastel1);

    var color = d3.scaleOrdinal(d3.schemeAccent); //window.pie_shared_color;//d3.scaleOrdinal(scheme || d3.schemeCategory20);   

    var svg = d3.select(this.$refs.chart)
      .append('svg')
      .attr('class', 'pie')
      //.attr('class', 'fleft')
      .attr('width', width)
      .attr('height', height);

    var g = svg.append('g')
      .style("cursor", "default")
      .attr('transform', 'translate(100, 100)');
      
    var arc = d3.arc()
      .outerRadius(radius - radius*0.3)
      .innerRadius(radius);      
      
    var pie = d3.pie()
      .value(function(d) { return d.value; })
      .sort(null);

    var lbl = (val) => {
      if(val < 10000){
        return val;
      } else {
        if(val< 1000000){
          return Math.round(val/1000, 1) + ' M'
        } else {
          return Math.round(val/1000000, 1) + ' MM'
        }
      }
    }

    var narc = (d) => {
      var i = d3.interpolate(this._current, d);    
      this._current = i(0);    
      return function(t) {
        return arc(i(t))
      }    
    }

    const tooltipGroup = svg
      .append('g')
      .attr('class', 'mtt')
   
      var data = this.data;
      let input;
      /*var kv = {}
      for( let i in input){
        let val = input[i];
        data.push({"name": this.decode[val[0]], "id": val[0], "value":val[1], "url": val[2], "summ": val[4]});
        kv[this.decode[val[0]]] = {"value":val[1], "summ": val[4]}
      };*/

      if(data.length == 0 && input == undefined){
        data.push({"name": 'Нет данных', "confirmation": 10, 'value': 0.1, 'summ': 0.1})
      }

      g.selectAll('path.pie')
        .data( pie(data) )
        .join('path')
        .attr('fill', (d,i) => d.data.value == '0.1'? 'lightgray': color(d.data.confirmation))
        .style('opacity', opacity)
        .style('stroke', 'white')        
        .attr('class', 'pie')
        .on('click', d => {
          if(d.data.url){
            window.open(d.data.url);
          }
        })
        .on('mousemove', d => {


          var others = svg.selectAll("path.pie").filter( (e) => {
              return e.data != d.data
          });
          others.style('opacity', 0.4);

          tooltipGroup
            .attr('transform', `translate(${ d3.event.layerX + 5 },${ d3.event.layerY + 5 })`);
        })
        .on('mouseenter', d => {
          tooltipGroup.append('text')
            .text(` ${d.data.name} (${ lbl(d.data[this.param]) })`)
            .style("font-size", "12px")
            .attr("alignment-baseline","middle");
          
          d3.selectAll('path.pie').filter( e => e.data == d.data)
          .style('cursor', 'pointer');  
        })
        .on('mouseleave', () => {
          tooltipGroup.select('text').remove();
          svg.selectAll("path.pie").style('opacity', opacity).style('cursor', 'default')
        });

      g.selectAll('path.pie')
        .transition()
        .duration(500)
        .attrTween('d', narc);
        
      g.selectAll('circle')  
        .data( data )      
        .join("circle")
        .attr("cx", 105 )
        .attr("cy", (d, i) => -75 + 15 * i)
        .attr("r", 6)
        .style("fill", (d,i) =>  d.value == '0.1'? 'lightgray': color(d.confirmation) )

      g.selectAll('text.legend')  
        .data( data )      
        .join("text")
        .attr("x", 115 )
        .attr("y", (d, i) => -75 + 15 * i)
        .text( (d, i) => d.name + " " + (data == undefined? "": " (" + lbl( d[this.param] ) + ')') )
        .style("font-size", "10px")
        .attr("alignment-baseline","middle")
        .attr('class', 'legend')
        .style('cursor', 'pointer')
        .on('mousemove', (d,i) => {
          svg.selectAll('text.legend').filter( e => e.name == d.name ).attr("text-decoration", "underline");

          var others = svg.selectAll("path.pie").filter( (e) => {
            return e.data.name != d.name
          });
          others.style('opacity', 0.4);

        })
        .on('mouseleave', (d, i) => {
          svg.selectAll('text.legend').filter( e => e.name == d.name ).attr("text-decoration", "");

          svg.selectAll("path.pie").style('opacity', opacity);

        })
        .on('click', d => {
          if(d.url){
            window.open(d.url);
          }
        })

      g.selectAll('text.header')
        .data( [this.idname] )
        .join('text')
        .attr("x", 100 )
        .attr("y", -90)
        .text( d => d + " (" + (data == undefined ? '0': lbl( data.reduce( (r,e) => r + e[this.param], 0)) ) + ")")
        .style("font-size", "12px")
        .attr("alignment-baseline","middle")
        .attr('class', 'header')
      }
      
    }
	

</script>

<style scoped>

</style>