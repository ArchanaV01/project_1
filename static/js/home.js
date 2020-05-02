function clickonBook(event) {
    event.preventDefault();
    var href = event.currentTarget.getAttribute('href');
    // Initialize new request
    const request = new XMLHttpRequest();
    bookURL = 'http://127.0.0.1:5000/api' + href;
    request.open('GET', bookURL);
    console.log("request open");
    // Callback function for when request completes
    request.send();
    request.onload = () => {
        console.log("request loaded");
        // Extract JSON data from request
        const data = JSON.parse(request.responseText);
        // Update the result div
        if (data['status'] == 200) {
            document.querySelector(".right_container").style.visibility = "visible";
            document.getElementById("myimg").src = "http://covers.openlibrary.org/b/isbn/" + data['isbn'] + "-M.jpg";
            console.log(document.getElementById("myimg").src);
            document.querySelector('#title').innerHTML = data['title'];
            document.querySelector('#author').innerHTML = "Author: " + data['author'];
            document.querySelector('#year').innerHTML = "Year: " + data['year'];
            document.querySelector('#isbn').innerHTML = "ISBN: " + data['isbn'];
            if (data['reviews'].length == 0) {
                document.querySelector("#review_scroll").innerHTML = "No Reviews given";
            } else {
                var str = ''
                data['reviews'].forEach(function (r) {
                    str += '<li>' + "'" + r['review'] + "' -" + r['name'] + ".   Rated: " + r['rating'] + '</li>';
                });
                document.querySelector("#review_scroll").innerHTML = str;
            }
        }
        else {
            document.querySelector(".right_container").style.visibility = "visible";
            document.querySelector('#result').innerHTML = 'No Book found. Invalid ISBN number';
        }
    }
};