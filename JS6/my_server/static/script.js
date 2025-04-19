person = {
    namn: "Bert",
    ålder: 27
}

const updateInfo = () => {
    $("#content").text(person.namn + " är " + person.ålder + " år");
}

$(document).ready(() => {
    updateInfo();

    $("#btn_sendrequest").click(() => {
        $.ajax({
            method: "POST",
            url: "/addoneyear",
            data: JSON.stringify(person),
            headers: {'Content-Type': 'application/json'},
            dataType: "json",
            success: (response) => {
                person.ålder = response.ålder;
                updateInfo();
            }
        })
    });
});
