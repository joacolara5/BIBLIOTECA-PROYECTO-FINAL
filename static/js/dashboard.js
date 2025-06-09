$(document).ready(function () {
  // Inicializar Select2
  $('#filterCategoria, #filterYear').select2({ theme: 'bootstrap-5', placeholder:'Seleccionar…', allowClear:true });

  // Eventos
  $('#filterCategoria, #filterYear').on('change', aplicarFiltrosYGraficos);
  $('#searchTitle').on('input', aplicarFiltrosYGraficos);
  $('#toggleTable').on('click', function(){
    $('#tablaContainer, #tableTitle').toggleClass('d-none');
    $(this).text( $('#tablaContainer').hasClass('d-none') ? 'Mostrar Tabla' : 'Ocultar Tabla' );
  });
  $('#toggleCharts').on('click', function(){
    $('#sectionCharts, #chartsTitle').toggleClass('d-none');
    $(this).text( $('#sectionCharts').hasClass('d-none') ? 'Mostrar Gráficos' : 'Ocultar Gráficos' );
  });
  $('#toggleTheme').on('click', function(){
    const html = document.documentElement;
    const isDark = html.getAttribute('data-bs-theme')==='dark';
    html.setAttribute('data-bs-theme', isDark?'light':'dark');
    $(this).text(isDark?'Modo Oscuro 🌙':'Modo Claro 🌞');
  });

  // Carga inicial
  allData.sort((a,b)=>a.year-b.year);
  popularFiltros();
  aplicarFiltrosYGraficos();
});

function popularFiltros(){
  const cats = [...new Set(allData.map(d=>d.categoria))].sort();
  const yrs = [...new Set(allData.map(d=>d.year))].sort();
  llenar('#filterCategoria', cats);
  llenar('#filterYear', yrs);
}
function llenar(sel, arr){
  const $s = $(sel).empty().append('<option/>');
  arr.forEach(v=>$s.append(`<option value="${v}">${v}</option>`));
  $s.trigger('change');
}

function aplicarFiltrosYGraficos(){
  const cat = $('#filterCategoria').val()||[];
  const yr  = $('#filterYear').val()||[];
  const txt = $('#searchTitle').val().toLowerCase();
  const filtered = allData.filter(d=>
    (cat.length===0||cat.includes(d.categoria)) &&
    (yr.length===0||yr.includes(String(d.year))) &&
    (!txt||d.titulo.toLowerCase().includes(txt))
  );
  actualizarStats(filtered);
  cargarTabla(filtered);
  renderGraficos(filtered);
}

function actualizarStats(data){
  $('#totalLibros').text(data.length);
  const cats = [...new Set(data.map(d=>d.categoria))].length;
  $('#totalCategorias').text(cats);
  // simulamos usuarios
  $('#totalUsuarios').text(40);
  // año con más entradas
  const countYr = {};
  data.forEach(d=>countYr[d.year]=(countYr[d.year]||0)+1);
  const top = Object.entries(countYr).sort((a,b)=>b[1]-a[1])[0]?.[0]||'N/A';
  $('#anioTop').text(top);
}

function cargarTabla(data){
  if($.fn.DataTable.isDataTable('#tablaLibros')){
    $('#tablaLibros').DataTable().clear().destroy();
  }
  $('#tablaLibros').DataTable({
    data: data.map(d=>[d.titulo,d.autor,d.categoria,d.year]),
    columns: [
      {title:"Título"}, {title:"Autor"}, {title:"Categoría"}, {title:"Año", className:"text-end"}
    ],
    responsive:true, autoWidth:false, pageLength:8,
    language:{search:"",lengthMenu:"Mostrar _MENU_",paginate:{next:"Siguiente",previous:"Anterior"}}
  });
}

let pieChart, barChart;
function renderGraficos(data){
  // Pie por categoría
  const cntCat = {};
  data.forEach(d=>cntCat[d.categoria]=(cntCat[d.categoria]||0)+1);
  const labs = Object.keys(cntCat), vals = labs.map(l=>cntCat[l]);
  pieChart?.destroy();
  pieChart = new Chart($('#pieCategoria'), {
    type:'pie', data:{labels:labs,datasets:[{data:vals}]},
    options:{plugins:{title:{display:true,text:'Libros por Categoría'}}}
  });

  // Bar por año
  const cntYr={}, yrs=[...new Set(data.map(d=>d.year))].sort((a,b)=>a-b);
  yrs.forEach(y=>cntYr[y]=(data.filter(d=>d.year===y).length));
  barChart?.destroy();
  barChart = new Chart($('#barAnio'), {
    type:'bar', data:{labels:yrs,datasets:[{label:'Libros',data:yrs.map(y=>cntYr[y])}]},
    options:{plugins:{title:{display:true,text:'Libros por Año'}},scales:{y:{beginAtZero:true}}}
  });
}
