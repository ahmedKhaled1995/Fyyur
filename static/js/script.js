window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

document.addEventListener("DOMContentLoaded", () => {
  // Defining a delete handler for deleting venues
  const deleteVenueHandler = async (e) => {
    const venueId = e.target.parentNode.getAttribute("data-id");
    try {
      await axios.delete(`/venues/${venueId}`);
      alert("Venue deleted successfully!");
      window.location.replace("/");
    } catch (e) {
      alert("Error deleteing venue!");
    }
  };
  // Adding the delete handler for deleting venues
  const venueDeleteLinks = [...document.querySelectorAll(".delete_venue")];
  venueDeleteLinks.forEach((item) => {
    item.addEventListener("click", deleteVenueHandler);
  });

  // Defining an edit handler for editing artists
  const editArtist = (e) => {
    const artistId = e.target.getAttribute("data-id");
    window.location.replace(`/artists/${artistId}/edit`);
  };
  // Adding the event handler to the edit artist button
  const editArtistButtons = [...document.querySelectorAll(".edit-artist")];
  editArtistButtons.forEach((item) => {
    item.addEventListener("click", editArtist);
  });

  // Defining an edit handler for editing venues
  const editVenue = (e) => {
    const venueId = e.target.getAttribute("data-id");
    console.log(venueId);
    window.location.replace(`/venues/${venueId}/edit`);
  };
  // Adding the event handler to the edit artist button
  const editVenueButtons = [...document.querySelectorAll(".edit-venue")];
  editVenueButtons.forEach((item) => {
    item.addEventListener("click", editVenue);
  });
});
