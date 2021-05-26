

export function download(data, filetype, filename){
    let blob = new Blob([data], { type: filetype ||"plain/text" });
    let url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    setTimeout( () => {
        link.remove();
    }, 100)
    URL.revokeObjectURL(url);
}