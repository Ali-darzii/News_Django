$(document).ready(function () {


    $('#togglelink').unbind().click(function (e) {
        e.preventDefault();
        console.log('w');
        var password = $('#pass_show');
        var pass_type = password.attr('type');
        if (pass_type === 'password') {
            password.attr('type', 'text');

        } else {
            password.attr('type', 'password');
        }
    });


    $("#uploadButton").on("click", function (e) {
        e.preventDefault();
        $("#imageInput").click();
    });

    $("#imageInput").on("change", function () {
        var file = $(this)[0].files[0];
        if (file) {
            $("#imagePreview").html(`<img src="${URL.createObjectURL(file)}" alt="Uploaded Image">`);
            $("#imageName").text(`Image Name: ${file.name}`);
            $("#deleteButton").show();

            var formData = new FormData();
            formData.append('image', file);

        }
    });

    $("#deleteButton").on("click", function (e) {
        e.preventDefault();
        $("#imagePreview").empty();
        $("#imageName").empty();
        $("#deleteButton").hide();
        $("#imageInput").val(""); // Clear the file input
    });


});