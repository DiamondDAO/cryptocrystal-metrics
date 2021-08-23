$(document).ready(function () {
  $("#fixed-tab-metrics")
    .find(".column1")
    .hover(
      function () {
        $(this)
          .css("cursor", "pointer")
          .attr("title", "The type/kind of crystal");
      },
      function () {
        $(this).css("cursor", "auto");
      }
    );

  $("#fixed-tab-metrics")
    .find(".column2")
    .hover(
      function () {
        $(this)
          .css("cursor", "pointer")
          .attr("title", "The real-world rarity of this crystal type");
      },
      function () {
        $(this).css("cursor", "auto");
      }
    );

  $("#fixed-tab-metrics")
    .find(".column3")
    .hover(
      function () {
        $(this)
          .css("cursor", "pointer")
          .attr("title", "The weight of the last sale of this crystal type");
      },
      function () {
        $(this).css("cursor", "auto");
      }
    );

  $("#fixed-tab-metrics")
    .find(".column4")
    .hover(
      function () {
        $(this)
          .css("cursor", "pointer")
          .attr(
            "title",
            "The price of the last sale of this crystal type (in Ξ)"
          );
      },
      function () {
        $(this).css("cursor", "auto");
      }
    );

  $("#fixed-tab-metrics")
    .find(".column5")
    .hover(
      function () {
        $(this)
          .css("cursor", "pointer")
          .attr("title", "The total weight in existence of this crystal type");
      },
      function () {
        $(this).css("cursor", "auto");
      }
    );

  $("#fixed-tab-metrics")
    .find(".column6")
    .hover(
      function () {
        $(this)
          .css("cursor", "pointer")
          .attr(
            "title",
            "The total value of this crystal type based on the last sale and average weight of these crystals"
          );
      },
      function () {
        $(this).css("cursor", "auto");
      }
    );

  $("#fixed-tab-metrics")
    .find(".column7")
    .hover(
      function () {
        $(this)
          .css("cursor", "pointer")
          .attr(
            "title",
            "The adjusted market cap based on the implied market cap as well as the weighted rarity and total market cap of cryptocrystals"
          );
      },
      function () {
        $(this).css("cursor", "auto");
      }
    );

  $("#fixed-tab-metrics")
    .find(".column8")
    .hover(
      function () {
        $(this)
          .css("cursor", "pointer")
          .attr(
            "title",
            "Adjusted unit price for crystal type, calculated as a weighted average of scarcities with the total market cap."
          );
      },
      function () {
        $(this).css("cursor", "auto");
      }
    );
});
