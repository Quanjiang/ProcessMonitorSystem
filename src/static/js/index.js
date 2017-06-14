  $(document).ready(function(){
        draw_table();
      });
      function draw_table(){
        var table = "<table><tr><th>INDEX</th><th>NAME_ID</th><th>STATUS</th><th>detail</th>"
        $.get("get_all",{},function (data){

           result = JSON.parse(data);
           if (result['err'] != 0){
             alert(result['msg'])
             return
           }
           result = result['list']
           for (var i = 0;i<result.length;i++){
            line = "<tr>"
            line += "<td>"+ i + "</td>"
            line += "<td>"+ result[i]["name_id"]+ "</td>"
            line += "<td>"+ result[i]["status"]+ "</td>"
            line += "<td><input type='button' value='go' onclick=\"if(confirm('确定跳转？')){location.href='/query?name_id="+result[i]['name_id']+"'}\"</td>"
            line+= "</tr>"
            table += line
           }
           table += "</table>"
           document.getElementById("table").innerHTML = table;
        })

      }