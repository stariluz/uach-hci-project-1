const API = "http://127.0.0.1:8000";

$("#hi-button").on("click", function (event) {
    $.ajax({
        url: `${API}`,
        success: function (result) {
            console.log(result.content);
            $("#hi-box").html("<strong>" + result.content + "</strong>");
        }
    });
});
