#  Description: Music Monolith Marketing Website
#  Author: Benjamin Orrvick
#  Author URL:  https://github.com/borrvick/
#  Purpose: Create a playlist object so it can be added to a list and each playlists datacan be used
#  Tags: Music, Marketing, Business, Website, Application


import re


class playlistObjects:
    def __init__(
        self,
        pPlaylistName,
        pPlaylistDescription,
        pPlaylistUrl,
        pProfile,
        pProfileUrl,
    ):
        self.playlistName = pPlaylistName
        self.playlistDescription = pPlaylistDescription
        self.playlistUrl = pPlaylistUrl
        self.profile = pProfile
        self.profileUrl = pProfileUrl

        self.email = self.findEmail(pPlaylistDescription)
        self.insta = self.findInsta(pPlaylistDescription)

    def findEmail(self, pEmail):
        # pattern to check for email
        emailMatch = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", pEmail)
        # this if prevents an error from happening if there is no email
        if emailMatch:
            return emailMatch.group(0)
        else:
            emailMatch = "None"
        return emailMatch

    def findInsta(self, pInsta):
        # assign the first search for full instagram link
        instamatchURL = re.search(
            r"(https://www\.instagram\.com/)([A-Za-z0-9_.]*)", pInsta
        )
        # this test passes under many scenerios of differnet ways of instagram handles being displayed in description
        instamatchHandle = re.search(
            r"(\binstagram\b|\big\b|\binsta\b)([\W]*\bis\b[\W]*[\W]*\bat\b[\W]*|[\W]*\bat\b[\W]*|[\W]*)([A-Za-z0-9_\.]*)",
            pInsta,
            re.I,
        )
        # find only handles with no instagram indication and ecludes cases where there is a space before
        # the @ assuming if there was a space, it would be an email
        # CONSIDER: if the @ handle is the first thing in description it doesnt work
        instamatchHandleOnly = re.search(
            r"([\s][@])([A-Za-z0-9_\.]*)", pInsta, re.I
        )
        if instamatchURL:
            return f"{instamatchURL.group(0)}/"
        # this is before instamatch handle because if opposite some cases would not beconsidered
        elif instamatchHandleOnly:
            return (
                f"https://www.instagram.com/{instamatchHandleOnly.group(2)}/"
            )
        elif instamatchHandle:
            return f"https://www.instagram.com/{instamatchHandle.group(3)}/"
        else:
            return "None"
