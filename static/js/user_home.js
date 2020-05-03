function searchResults(event) {
    // document.querySelector("#Card").style.visibility = "hidden";
    document.querySelector(".right_container").style.visibility = "hidden";
    event.preventDefault();
    const key = document.getElementById("key").value;
    const category = document.getElementById("category").value;
    var req = new XMLHttpRequest();
    var url = "/api/search?key=" + key + "&category=" + category;
    console.log(url);
    req.open("GET", url);
    req.send();
    req.onload = function() {
        document.querySelector(".left_container").style.visibility = "visible";
        if (req.status === 200) {

            document.querySelector("#resultsTable").style.visibility = "visible";
            var books = JSON.parse(req.responseText);
            var content = "";
            for (index in books) {
                each_book = books[index];
                // console.log(each_book["title"]);
                content += "<tr> <td><a id=bookURL onclick='clickonBook(event)' href='/book/" + each_book["isbn"] + "'>" + each_book["title"] + "</a> </td> <td>" + each_book["author"] + "</td><td>" + each_book["year"] + "</td></tr>";
            }
            // console.log(content);
            document.querySelector("#searchResults").innerHTML = content;
        } else {
            document.querySelector(".left_container").innerHTML = "<h2>No Search Results</h2>";
        }
    }
}

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
                data['reviews'].forEach(function(r) {
                    str += '<li>' + "'" + r['review'] + "' -" + r['name'] + ".   Rated: " + r['rating'] + '</li>';
                });
                document.querySelector("#review_scroll").innerHTML = str;
            }
        } else {
            document.querySelector(".right_container").style.visibility = "visible";
            document.querySelector('#result').innerHTML = 'No Book found. Invalid ISBN number';
        }
    }
};