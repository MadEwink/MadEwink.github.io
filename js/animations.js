var first_objective = 1;
var second_objective= 1;

function testAnimate() {
	var value = document.getElementById("one-tile-slider").value;
	var first_ring = document.getElementById("first-ring");
	var second_ring = document.getElementById("second-ring");
	var first_opacity = Number(first_ring.getAttribute("opacity"));
	var second_opacity = Number(second_ring.getAttribute("opacity"));
	if (value == 2) {
		first_objective = 1;
		second_objective = 1;
	} else if (value == 1) {
		first_objective = 1;
		second_objective = 0;
	} else {
		first_objective = 0;
		second_objective = 0;
	}
	var id = setInterval(changeOpacity, 20);
	function changeOpacity() {
		console.log("test");
		if (first_opacity == first_objective && second_opacity == second_objective) {
			clearInterval(id);
		} else {
			if (first_opacity < first_objective) {
				first_opacity += 0.1;
				if (first_opacity > first_objective)
					first_opacity = first_objective;
			} else if (first_opacity > first_objective) {
				first_opacity -= 0.1;
				if (first_opacity < first_objective)
					first_opacity = first_objective;
			}
			if (second_opacity < second_objective) {
				second_opacity += 0.1;
				if (second_opacity > second_objective)
					second_opacity = second_objective;
			} else if (second_opacity > second_objective) {
				second_opacity -= 0.1;
				if (second_opacity < second_objective)
					second_opacity = second_objective;
			}
			first_ring.setAttribute("opacity", first_opacity);
			second_ring.setAttribute("opacity", second_opacity);
		}
	}
}


