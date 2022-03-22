// Author: Ben Orrvick
// Company: MusicMonolithic
// Date: 02/24/2022
// Purpose: Javascript file that has a function to show and unshow the loader



// creates displays loader only works on button click
function Loader() {
    if (document.getElementById("search-bar").value.length > 0) {
        document.getElementById("base-div").style.display = "none";
        document.getElementById("loader-div").style.display = "flex";
        document.getElementById("video-background").style.display = "none";
    }
}