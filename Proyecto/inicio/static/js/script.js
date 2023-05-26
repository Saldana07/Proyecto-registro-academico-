$(document).ready(function() {
  // Inicializar DataTables
  var tabla = $('#dataTable').DataTable();

  // Configurar el buscador
  $('#buscar').on('keyup', function() {
    tabla.search(this.value).draw();
  });

  // Configurar la opción de selección de cantidad de elementos a mostrar
  $('#cantidad-elementos').on('change', function() {
    tabla.page.len(this.value).draw();
  });

    // Realizar solicitud AJAX para obtener los datos de disponibilidad
    $.ajax({
      url: 'ruta/para/obtener/datos/disponibilidad',
      method: 'GET',
      success: function(response) {
        // Construir la tabla dinámica
        var tabla = $('<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0"></table>');
        var thead = $('<thead><tr><th>Fecha</th><th>Hora de inicio</th><th>Hora de fin</th><th>Comentarios</th><th>Editar</th><th>Usuario</th></tr></thead>');
        var tbody = $('<tbody></tbody>');
  
        // Recorrer los datos de disponibilidad y agregar filas a la tabla
        for (var i = 0; i < response.length; i++) {
          var disponibilidad = response[i];
          var fila = $('<tr></tr>');
          fila.append('<td>' + disponibilidad.usuario_nombre + '</td>');
          fila.append('<td>' + disponibilidad.fecha + '</td>');
          fila.append('<td>' + disponibilidad.hora_inicio + '</td>');
          fila.append('<td>' + disponibilidad.hora_fin + '</td>');
          fila.append('<td>' + disponibilidad.comentarios + '</td>');
          fila.append('<td><a class="text-danger" href="' + disponibilidad.url_editar + '">Editar</a></td>');
         
          tbody.append(fila);
        }
  
        tabla.append(thead);
        tabla.append(tbody);
  
        tablaDisponibilidad.append(tabla);
      },
      error: function(xhr, status, error) {
        console.error(error);
      }
    });
  });
  