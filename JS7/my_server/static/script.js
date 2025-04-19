const updateResults = (response) => {
    $("#personal").empty();

    console.log(response['result']);
    if (!response['result'] || response['result'].length === 0) return;

    let table = document.createElement("table");
    let titles = document.createElement("tr");
    
    let name = document.createElement("th");
    let telephone = document.createElement("th");
    let salary = document.createElement("th");

    name.innerHTML = "Name";
    telephone.innerHTML = "Telephone";
    salary.innerHTML = "Salary";

    titles.appendChild(name);
    titles.appendChild(telephone);
    titles.appendChild(salary);

    table.appendChild(titles);

    for (const person of response['result']) {
        let tr = document.createElement("tr");
    
        let nameTd = document.createElement("td");
        nameTd.innerHTML = person[0];
        tr.appendChild(nameTd);
    
        let telephoneTd = document.createElement("td");
        telephoneTd.innerHTML = person[1];
        tr.appendChild(telephoneTd);
    
        let salaryTd = document.createElement("td");
        salaryTd.innerHTML = person[2];
        tr.appendChild(salaryTd);
    
        table.appendChild(tr);
    }

    $('#personal').append(table);
}

const query = (searchValue, departmentValue) => {
    $.ajax({
        method: 'POST',
        url: '/search',
        data: JSON.stringify({ search: searchValue, department: departmentValue }),
        headers: {'Content-Type': 'application/json'},
        dataType: 'json',
        success: (response) => updateResults(response)
    });
}

function departmentSearch(id) {
    query("", id);
}

$(document).ready(() => {

    $("#search").on('input', function() {
        let value = $(this).val();

        if (!value) {
            $("#personal").empty();
            return;
        } 

        query(value, "all");
    });

    $("#btn_h").click(() => departmentSearch("h"));
    $("#btn_s").click(() => departmentSearch("s"));
    $("#btn_d").click(() => departmentSearch("c"));
});