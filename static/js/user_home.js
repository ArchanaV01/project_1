function searchResults(event) {
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
                content += "<tr> <td><a href='/book_page/" + each_book["isbn"] + "'>" + each_book["title"] + "</a> </td> <td>" + each_book["author"] + "</td><td>" + each_book["year"] + "</td></tr>";
            }
            // console.log(content);
            document.querySelector("#searchResults").innerHTML = content;
        } else {
            document.querySelector(".left_container").innerHTML = "<h2>No Search Results</h2>";
        }
    }
}