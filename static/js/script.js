window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

document.addEventListener("DOMContentLoaded", () => {
  console.log("Page loaded");

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
});
