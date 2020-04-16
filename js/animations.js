var first_objective = 1;
var second_objective= 1;

function initAllAnimations() {
	displayJSOnly();
	initOneTile();
	initFirstGeneration();
	initObjectGeneration();
}

function displayJSOnly() {
	var elements = document.getElementsByClassName("js-only");
	for (var i = 0 ; i < elements.length ; i++) {
		elements[i].removeAttribute("style");
	}
}

function initOneTile() {
}

function animateOneTile() {
	var value = document.getElementById("one-tile-slider").value;
	var valueIndicator = document.getElementById("one-tile-value");
	valueIndicator.innerHTML = value;
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

var tileObjectives = new Array(19);
var tileOpacities = new Array(19);
var tiles = new Array(19);

for (var i = 0 ; i < tileObjectives.length ; i++) {
	tileObjectives[i] = 0;
}

function initFirstGeneration() {
	var svg = document.getElementById("first-generation");
	for (var i = 0 ; i < tileObjectives.length ; i++) {
		tiles[i] = svg.querySelector("#tile-"+i)
		tiles[i].setAttribute("opacity", 0);
	}
	var slider = document.getElementById("first-generation-slider");
	slider.value = 0;
	var valueIndicator = document.getElementById("first-generation-value");
	valueIndicator.innerHTML = slider.value;
}

function animateFirstGeneration() {
	var value = document.getElementById("first-generation-slider").value;
	var valueIndicator = document.getElementById("first-generation-value");
	valueIndicator.innerHTML = value;
	var svg = document.getElementById("first-generation");
	for (var i = 0 ; i < tileObjectives.length ; i++) {
		tileObjectives[i] = (i<value)?1:0;
		tiles[i] = svg.querySelector("#tile-"+i)
		tiles[i].setAttribute("fill", (i+1==value)?"red":"");
		tileOpacities[i] = Number(tiles[i].getAttribute("opacity"));
	}
	var id = setInterval(changeOpacity, 20);
	function changeOpacity() {
		var finished = true;
		for (var i = 0 ; i < tileObjectives.length ; i++) {
			if (tileOpacities[i] < tileObjectives[i]) {
				finished = false;
				tileOpacities[i] += 0.1;
				if (tileOpacities[i] > tileObjectives[i])
					tileOpacities[i] = tileObjectives[i];
			} else if (tileOpacities[i] > tileObjectives[i]) {
				finished = false;
				tileOpacities[i] -= 0.1;
				if (tileOpacities[i] < tileObjectives[i])
					tileOpacities[i] = tileObjectives[i];
			}
			tiles[i].setAttribute("opacity", tileOpacities[i]);
		}
		if (finished)
			clearInterval(id);
	}
}

function initObjectGeneration() {
	var slider = document.getElementById("object-generation-slider");
	slider.value = 0;
	var valueIndicator = document.getElementById("object-generation-value");
	valueIndicator.innerHTML = slider.value;
	var svg = document.getElementById("object-generation");
	var centerTile = svg.querySelector("#tile-0");
	var firstRing = svg.querySelector("#ring-1");
	var secondRing = svg.querySelector("#ring-2");
	centerTile.setAttribute("fill", "white");
	firstRing.setAttribute("fill", "white");
	secondRing.setAttribute("fill", "white");
}
function animateObjectGeneration() {
	var value = Number(document.getElementById("object-generation-slider").value);
	var valueIndicator = document.getElementById("object-generation-value");
	valueIndicator.innerHTML = value;
	var svg = document.getElementById("object-generation");
	var centerTile = svg.querySelector("#tile-0");
	var firstRing = svg.querySelector("#ring-1");
	var secondRing = svg.querySelector("#ring-2");
	switch(value) {
		case 0:
			centerTile.setAttribute("fill", "white");
			firstRing.setAttribute("fill", "white");
			secondRing.setAttribute("fill", "white");
			break;
		case 1:
			centerTile.setAttribute("fill", "grey");
			firstRing.setAttribute("fill", "white");
			secondRing.setAttribute("fill", "white");
			break;
		case 2:
			centerTile.setAttribute("fill", "grey");
			firstRing.setAttribute("fill", "grey");
			secondRing.setAttribute("fill", "white");
			break;
		case 3:
			centerTile.setAttribute("fill", "red");
			firstRing.setAttribute("fill", "grey");
			secondRing.setAttribute("fill", "white");
			break;
		case 4:
			centerTile.setAttribute("fill", "red");
			firstRing.setAttribute("fill", "grey");
			secondRing.setAttribute("fill", "grey");
			break;
		case 5:
			centerTile.setAttribute("fill", "red");
			firstRing.setAttribute("fill", "red");
			secondRing.setAttribute("fill", "grey");
			break;
		case 6:
			centerTile.setAttribute("fill", "green");
			firstRing.setAttribute("fill", "red");
			secondRing.setAttribute("fill", "grey");
			break;
		default:
			break;
	}
}
