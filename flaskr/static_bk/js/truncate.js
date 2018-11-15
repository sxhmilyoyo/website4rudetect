jQuery(document).ready(function( $ ) {

   $(".font-weight-light").dotdotdot({

      callback: function( isTruncated ) {},
      /* Function invoked after truncating the text.
         Inside this function, "this" refers to the wrapper. */

      ellipsis: "\u2026 ",
      /* The text to add as ellipsis. */

      height: null,
      /* The (max-)height for the wrapper:
         null: measure the CSS (max-)height ones;
         a number: sets a specific height in pixels;
         "watch": re-measures the CSS (max-)height in the "watch". */

      keep: null,
      /* jQuery-selector for elements to keep after the ellipsis. */

      tolerance: 0,
      /* Deviation for the measured wrapper height. */

      truncate: "word",
      /* How to truncate the text: By "node", "word" or "letter". */

      watch: "window",
      /* Whether to update the ellipsis:
         true: Monitors the wrapper width and height;
         "window": Monitors the window width and height. */

   });
});
