
/*!

=========================================================
* Argon Dashboard - v1.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard
* Copyright 2020 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard/blob/master/LICENSE.md)

* Coded by www.creative-tim.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/



//
// Layout
//

'use strict';

var Layout = (function () {

	function pinSidenav() {
		$('.sidenav-toggler').addClass('active');
		$('.sidenav-toggler').data('action', 'sidenav-unpin');
		$('body').removeClass('g-sidenav-hidden').addClass('g-sidenav-show g-sidenav-pinned');
		$('body').append('<div class="backdrop d-xl-none" data-action="sidenav-unpin" data-target=' + $('#sidenav-main').data('target') + ' />');

		// Store the sidenav state in a cookie session
		Cookies.set('sidenav-state', 'pinned');
	}

	function unpinSidenav() {
		$('.sidenav-toggler').removeClass('active');
		$('.sidenav-toggler').data('action', 'sidenav-pin');
		$('body').removeClass('g-sidenav-pinned').addClass('g-sidenav-hidden');
		$('body').find('.backdrop').remove();

		// Store the sidenav state in a cookie session
		Cookies.set('sidenav-state', 'unpinned');
	}

	// Set sidenav state from cookie

	var $sidenavState = Cookies.get('sidenav-state') ? Cookies.get('sidenav-state') : 'pinned';

	if ($(window).width() > 1200) {
		if ($sidenavState == 'pinned') {
			pinSidenav()
		}

		if (Cookies.get('sidenav-state') == 'unpinned') {
			unpinSidenav()
		}

		$(window).resize(function () {
			if ($('body').hasClass('g-sidenav-show') && !$('body').hasClass('g-sidenav-pinned')) {
				$('body').removeClass('g-sidenav-show').addClass('g-sidenav-hidden');
			}
		})
	}

	if ($(window).width() < 1200) {
		$('body').removeClass('g-sidenav-hide').addClass('g-sidenav-hidden');
		$('body').removeClass('g-sidenav-show');
		$(window).resize(function () {
			if ($('body').hasClass('g-sidenav-show') && !$('body').hasClass('g-sidenav-pinned')) {
				$('body').removeClass('g-sidenav-show').addClass('g-sidenav-hidden');
			}
		})
	}



	$("body").on("click", "[data-action]", function (e) {

		e.preventDefault();

		var $this = $(this);
		var action = $this.data('action');
		var target = $this.data('target');


		// Manage actions

		switch (action) {
			case 'sidenav-pin':
				pinSidenav();
				break;

			case 'sidenav-unpin':
				unpinSidenav();
				break;

			case 'search-show':
				target = $this.data('target');
				$('body').removeClass('g-navbar-search-show').addClass('g-navbar-search-showing');

				setTimeout(function () {
					$('body').removeClass('g-navbar-search-showing').addClass('g-navbar-search-show');
				}, 150);

				setTimeout(function () {
					$('body').addClass('g-navbar-search-shown');
				}, 300)
				break;

			case 'search-close':
				target = $this.data('target');
				$('body').removeClass('g-navbar-search-shown');

				setTimeout(function () {
					$('body').removeClass('g-navbar-search-show').addClass('g-navbar-search-hiding');
				}, 150);

				setTimeout(function () {
					$('body').removeClass('g-navbar-search-hiding').addClass('g-navbar-search-hidden');
				}, 300);

				setTimeout(function () {
					$('body').removeClass('g-navbar-search-hidden');
				}, 500);
				break;
		}
	})


	// Add sidenav modifier classes on mouse events

	$('.sidenav').on('mouseenter', function () {
		if (!$('body').hasClass('g-sidenav-pinned')) {
			$('body').removeClass('g-sidenav-hide').removeClass('g-sidenav-hidden').addClass('g-sidenav-show');
		}
	})

	$('.sidenav').on('mouseleave', function () {
		if (!$('body').hasClass('g-sidenav-pinned')) {
			$('body').removeClass('g-sidenav-show').addClass('g-sidenav-hide');

			setTimeout(function () {
				$('body').removeClass('g-sidenav-hide').addClass('g-sidenav-hidden');
			}, 300);
		}
	})


	// Make the body full screen size if it has not enough content inside
	$(window).on('load resize', function () {
		if ($('body').height() < 800) {
			$('body').css('min-height', '100vh');
			$('#footer-main').addClass('footer-auto-bottom')
		}
	})

})();

//
// Charts
//

'use strict';

var Charts = (function () {

	// Variable

	var $toggle = $('[data-toggle="chart"]');
	var mode = 'light';//(themeMode) ? themeMode : 'light';
	var fonts = {
		base: 'Open Sans'
	}

	// Colors
	var colors = {
		gray: {
			100: '#f6f9fc',
			200: '#e9ecef',
			300: '#dee2e6',
			400: '#ced4da',
			500: '#adb5bd',
			600: '#8898aa',
			700: '#525f7f',
			800: '#32325d',
			900: '#212529'
		},
		theme: {
			'default': '#172b4d',
			'primary': '#5e72e4',
			'secondary': '#f4f5f7',
			'info': '#11cdef',
			'success': '#2dce89',
			'danger': '#f5365c',
			'warning': '#fb6340'
		},
		black: '#12263F',
		white: '#FFFFFF',
		transparent: 'transparent',
	};


	// Methods

	// Chart.js global options
	function chartOptions() {

		// Options
		var options = {
			defaults: {
				global: {
					responsive: true,
					maintainAspectRatio: false,
					defaultColor: (mode == 'dark') ? colors.gray[700] : colors.gray[600],
					defaultFontColor: (mode == 'dark') ? colors.gray[700] : colors.gray[600],
					defaultFontFamily: fonts.base,
					defaultFontSize: 13,
					layout: {
						padding: 0
					},
					legend: {
						display: false,
						position: 'bottom',
						labels: {
							usePointStyle: true,
							padding: 16
						}
					},
					elements: {
						point: {
							radius: 0,
							backgroundColor: colors.theme['primary']
						},
						line: {
							tension: .4,
							borderWidth: 4,
							borderColor: colors.theme['primary'],
							backgroundColor: colors.transparent,
							borderCapStyle: 'rounded'
						},
						rectangle: {
							backgroundColor: colors.theme['warning']
						},
						arc: {
							backgroundColor: colors.theme['primary'],
							borderColor: (mode == 'dark') ? colors.gray[800] : colors.white,
							borderWidth: 4
						}
					},
					tooltips: {
						enabled: true,
						mode: 'index',
						intersect: false,
					}
				},
				doughnut: {
					cutoutPercentage: 83,
					legendCallback: function (chart) {
						var data = chart.data;
						var content = '';

						data.labels.forEach(function (label, index) {
							var bgColor = data.datasets[0].backgroundColor[index];

							content += '<span class="chart-legend-item">';
							content += '<i class="chart-legend-indicator" style="background-color: ' + bgColor + '"></i>';
							content += label;
							content += '</span>';
						});

						return content;
					}
				}
			}
		}

		// yAxes
		Chart.scaleService.updateScaleDefaults('linear', {
			gridLines: {
				borderDash: [2],
				borderDashOffset: [2],
				color: (mode == 'dark') ? colors.gray[900] : colors.gray[300],
				drawBorder: false,
				drawTicks: false,
				drawOnChartArea: true,
				zeroLineWidth: 0,
				zeroLineColor: 'rgba(0,0,0,0)',
				zeroLineBorderDash: [2],
				zeroLineBorderDashOffset: [2]
			},
			ticks: {
				beginAtZero: true,
				padding: 10,
				callback: function (value) {
					if (!(value % 10)) {
						return value
					}
				}
			}
		});

		// xAxes
		Chart.scaleService.updateScaleDefaults('category', {
			gridLines: {
				drawBorder: false,
				drawOnChartArea: false,
				drawTicks: false
			},
			ticks: {
				padding: 20
			},
			maxBarThickness: 10
		});

		return options;

	}

	// Parse global options
	function parseOptions(parent, options) {
		for (var item in options) {
			if (typeof options[item] !== 'object') {
				parent[item] = options[item];
			} else {
				parseOptions(parent[item], options[item]);
			}
		}
	}

	// Push options
	function pushOptions(parent, options) {
		for (var item in options) {
			if (Array.isArray(options[item])) {
				options[item].forEach(function (data) {
					parent[item].push(data);
				});
			} else {
				pushOptions(parent[item], options[item]);
			}
		}
	}

	// Pop options
	function popOptions(parent, options) {
		for (var item in options) {
			if (Array.isArray(options[item])) {
				options[item].forEach(function (data) {
					parent[item].pop();
				});
			} else {
				popOptions(parent[item], options[item]);
			}
		}
	}

	// Toggle options
	function toggleOptions(elem) {
		var options = elem.data('add');
		var $target = $(elem.data('target'));
		var $chart = $target.data('chart');

		if (elem.is(':checked')) {

			// Add options
			pushOptions($chart, options);

			// Update chart
			$chart.update();
		} else {

			// Remove options
			popOptions($chart, options);

			// Update chart
			$chart.update();
		}
	}

	// Update options
	function updateOptions(elem) {
		var options = elem.data('update');
		var $target = $(elem.data('target'));
		var $chart = $target.data('chart');

		// Parse options
		parseOptions($chart, options);

		// Toggle ticks
		toggleTicks(elem, $chart);

		// Update chart
		$chart.update();
	}

	// Toggle ticks
	function toggleTicks(elem, $chart) {

		if (elem.data('prefix') !== undefined || elem.data('prefix') !== undefined) {
			var prefix = elem.data('prefix') ? elem.data('prefix') : '';
			var suffix = elem.data('suffix') ? elem.data('suffix') : '';

			// Update ticks
			$chart.options.scales.yAxes[0].ticks.callback = function (value) {
				if (!(value % 10)) {
					return prefix + value + suffix;
				}
			}

			// Update tooltips
			$chart.options.tooltips.callbacks.label = function (item, data) {
				var label = data.datasets[item.datasetIndex].label || '';
				var yLabel = item.yLabel;
				var content = '';

				if (data.datasets.length > 1) {
					content += '<span class="popover-body-label mr-auto">' + label + '</span>';
				}

				content += '<span class="popover-body-value">' + prefix + yLabel + suffix + '</span>';
				return content;
			}

		}
	}


	// Events

	// Parse global options
	if (window.Chart) {
		parseOptions(Chart, chartOptions());
	}

	// Toggle options
	$toggle.on({
		'change': function () {
			var $this = $(this);

			if ($this.is('[data-add]')) {
				toggleOptions($this);
			}
		},
		'click': function () {
			var $this = $(this);

			if ($this.is('[data-update]')) {
				updateOptions($this);
			}
		}
	});


	// Return

	return {
		colors: colors,
		fonts: fonts,
		mode: mode
	};

})();

//
// Icon code copy/paste
//

'use strict';

var CopyIcon = (function () {

	// Variables

	var $element = '.btn-icon-clipboard',
		$btn = $($element);


	// Methods

	function init($this) {
		$this.tooltip().on('mouseleave', function () {
			// Explicitly hide tooltip, since after clicking it remains
			// focused (as it's a button), so tooltip would otherwise
			// remain visible until focus is moved away
			$this.tooltip('hide');
		});

		var clipboard = new ClipboardJS($element);

		clipboard.on('success', function (e) {
			$(e.trigger)
				.attr('title', 'Copied!')
				.tooltip('_fixTitle')
				.tooltip('show')
				.attr('title', 'Copy to clipboard')
				.tooltip('_fixTitle')

			e.clearSelection()
		});
	}


	// Events
	if ($btn.length) {
		init($btn);
	}

})();

//
// Navbar
//

'use strict';

var Navbar = (function () {

	// Variables

	var $nav = $('.navbar-nav, .navbar-nav .nav');
	var $collapse = $('.navbar .collapse');
	var $dropdown = $('.navbar .dropdown');

	// Methods

	function accordion($this) {
		$this.closest($nav).find($collapse).not($this).collapse('hide');
	}

	function closeDropdown($this) {
		var $dropdownMenu = $this.find('.dropdown-menu');

		$dropdownMenu.addClass('close');

		setTimeout(function () {
			$dropdownMenu.removeClass('close');
		}, 200);
	}


	// Events

	$collapse.on({
		'show.bs.collapse': function () {
			accordion($(this));
		}
	})

	$dropdown.on({
		'hide.bs.dropdown': function () {
			closeDropdown($(this));
		}
	})

})();


//
// Navbar collapse
//


var NavbarCollapse = (function () {

	// Variables

	var $nav = $('.navbar-nav'),
		$collapse = $('.navbar .navbar-custom-collapse');


	// Methods

	function hideNavbarCollapse($this) {
		$this.addClass('collapsing-out');
	}

	function hiddenNavbarCollapse($this) {
		$this.removeClass('collapsing-out');
	}


	// Events

	if ($collapse.length) {
		$collapse.on({
			'hide.bs.collapse': function () {
				hideNavbarCollapse($collapse);
			}
		})

		$collapse.on({
			'hidden.bs.collapse': function () {
				hiddenNavbarCollapse($collapse);
			}
		})
	}

	var navbar_menu_visible = 0;

	$(".sidenav-toggler").click(function () {
		if (navbar_menu_visible == 1) {
			$('body').removeClass('nav-open');
			navbar_menu_visible = 0;
			$('.bodyClick').remove();

		} else {

			var div = '<div class="bodyClick"></div>';
			$(div).appendTo('body').click(function () {
				$('body').removeClass('nav-open');
				navbar_menu_visible = 0;
				$('.bodyClick').remove();

			});

			$('body').addClass('nav-open');
			navbar_menu_visible = 1;

		}

	});

})();

//
// Popover
//

'use strict';

var Popover = (function () {

	// Variables

	var $popover = $('[data-toggle="popover"]'),
		$popoverClass = '';


	// Methods

	function init($this) {
		if ($this.data('color')) {
			$popoverClass = 'popover-' + $this.data('color');
		}

		var options = {
			trigger: 'focus',
			template: '<div class="popover ' + $popoverClass + '" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'
		};

		$this.popover(options);
	}


	// Events

	if ($popover.length) {
		$popover.each(function () {
			init($(this));
		});
	}

})();

//
// Scroll to (anchor links)
//

'use strict';

var ScrollTo = (function () {

	//
	// Variables
	//

	var $scrollTo = $('.scroll-me, [data-scroll-to], .toc-entry a');


	//
	// Methods
	//

	function scrollTo($this) {
		var $el = $this.attr('href');
		var offset = $this.data('scroll-to-offset') ? $this.data('scroll-to-offset') : 0;
		var options = {
			scrollTop: $($el).offset().top - offset
		};

		// Animate scroll to the selected section
		$('html, body').stop(true, true).animate(options, 600);

		event.preventDefault();
	}


	//
	// Events
	//

	if ($scrollTo.length) {
		$scrollTo.on('click', function (event) {
			scrollTo($(this));
		});
	}

})();

//
// Tooltip
//

'use strict';

var Tooltip = (function () {

	// Variables

	var $tooltip = $('[data-toggle="tooltip"]');


	// Methods

	function init() {
		$tooltip.tooltip();
	}


	// Events

	if ($tooltip.length) {
		init();
	}

})();

//
// Form control
//

'use strict';

var FormControl = (function () {

	// Variables

	var $input = $('.form-control');


	// Methods

	function init($this) {
		$this.on('focus blur', function (e) {
			$(this).parents('.form-group').toggleClass('focused', (e.type === 'focus'));
		}).trigger('blur');
	}


	// Events

	if ($input.length) {
		init($input);
	}

})();

//
// Profile Page
//
function getAndSetProfileData(id) {
	$.ajax({
		url: '/get_profile_data/',
		type: 'GET',
		data: {
			'id': id
		},
		dataType: 'json',
		success: function (data) {
			loadProfileData(data);
		},
		failure: function () {
			alert('Error');
		}
	});
}

function loadProfileData(profileData) {
	document.getElementById("profile-name").innerHTML = "Bienvenido " + profileData.name;
	document.getElementById("profile-wallet").innerHTML = profileData.countLoad;
	document.getElementById("profile-properties").innerHTML = profileData.countProperties;
	document.getElementById("profile-properties-avg").innerHTML = Math.round(profileData.countProperties / profileData.countLoad);
	createProfileTable(profileData)
}

function loadCadastreInfo(loadId) {
	$.ajax({
		url: '/load_cadastre_info/',
		type: 'GET',
		data: {
			'id': loadId
		},
		dataType: 'json',
		success: function (data) {
			alert('Se ha cargado la información catastral sobre: ' + data + ' viviendas');
			getAndSetProfileData(2);
		},
		statusCode: {
			500: function () {
				alert("Se ha producido un error");
			}
		}
	});
}

function predictLoad(loadId) {
	$.ajax({
		url: '/predict_load/',
		type: 'GET',
		data: {
			'id': loadId
		},
		dataType: 'json',
		success: function (data) {
			alert('Se han estimado los precios')
		},
		statusCode: {
			500: function () {
				alert("Se ha producido un error");
			}
		}
	});
}

function createDomElement(tag, classes = null, innerHtml = null, id = null, style = null) {
	var domElement = document.createElement(tag);
	if (classes) {
		domElement.setAttribute("class", classes);
	}
	if (innerHtml) {
		domElement.innerHTML = innerHtml;
	}
	if (id) {
		domElement.setAttribute('id', id);
	}
	if (style) {
		domElement.setAttribute('style', style);
	}
	return domElement;

}

function createProfileTable(data) {
	var table = document.getElementById('profile-table-load');
	table.innerHTML = '';
	data.loads.forEach(function (load) {
		var tr = createDomElement('tr');

		var tdName = createDomElement('td', null,
			'<span style="cursor:pointer;">' + load.load__name + '</span>');
		var tdDate = createDomElement('td', null, load.load__date);
		var tdCount = createDomElement('td', null, load.count);
		var tdLoadPredictions = createDomElement('td', null,
			'<span style="cursor:pointer;"> Estimar </span>');
		tdLoadPredictions.onclick = function () {
			predictLoad(load.load__id);
		}
		var trResume = createDomElement('tr', null, null, 'table-load-resume-' + load.load__id);
		trResume.setAttribute('hidden', true);
		var tdResume = createDomElement('td')
		tdResume.setAttribute('colspan', 3);

		var tableResume = createDomElement('table', 'table align-items-center table-flush');
		var theadResume = createDomElement('thead', 'thead-light',
			'<tr>' +
			'<th>Fuente</th>' +
			'<th>Estado Viviendas</th>' +
			'<th></th>' +
			'</tr>'
		)
		var tbodyResume = createDomElement('tbody', 'list')

		var trCadastre = createDomElement('tr');
		var tdResumeSource = createDomElement('td', null, "Catastro");
		var tdResumeCount = createDomElement('td', null, load.not_null_count + " de " + load.count);
		var tdResumeLoad = createDomElement('td', null, '<span class="btn-link" style="cursor:pointer;">Cargar</span>', null);
		tdResumeLoad.onclick = function () {
			loadCadastreInfo(load.load__id);
		}
		trCadastre.appendChild(tdResumeSource);
		trCadastre.appendChild(tdResumeCount);
		trCadastre.appendChild(tdResumeLoad);

		tbodyResume.appendChild(trCadastre);
		tableResume.appendChild(theadResume);
		tableResume.appendChild(tbodyResume);
		tdResume.appendChild(tableResume);
		trResume.appendChild(tdResume);

		tdName.onclick = function () {
			var resume = document.getElementById('table-load-resume-' + load.load__id);
			if (resume.hasAttribute('hidden')) {
				resume.removeAttribute('hidden');
			} else {
				resume.setAttribute('hidden', true);
			}

		}
		tr.appendChild(tdName);
		tr.appendChild(tdDate);
		tr.appendChild(tdCount);
		tr.appendChild(tdLoadPredictions);

		table.appendChild(tr);
		table.appendChild(trResume);
	});
}

//
// Map Page
//
function getAndSetMapData(id) {
	$.ajax({
		url: '/get_map_data/',
		type: 'GET',
		data: {
			'id': id
		},
		dataType: 'json',
		success: function (data) {
			loadMapData(data);
		},
		failure: function () {
			alert('Error');
		}
	});
}

function loadMapData(mapData) {
	var lastHistoric = JSON.parse(mapData.lastHistoric)[0].fields
	var center = {};
	var zoom = 0;
	updateParentInfo(mapData.geoParent.name, mapData.geoParent.level)
	updateMapCart("actualPrice", lastHistoric.price);
	updateMapCartPercentage("monthlyVariation", lastHistoric.monthly_variation);
	updateMapCartPercentage("quarterlyVariation", lastHistoric.quarterly_variation);
	updateMapCartPercentage("annualVariation", lastHistoric.annual_variation);
	if (mapData.geoParent.level == "Distrito") {
		center = mapData.geoParent.centroid;
		zoom = 13;
		document.getElementById("seeMuncipality").removeAttribute("hidden");
	} else {
		center = default_center;
		zoom = default_zoom;
		document.getElementById("seeMuncipality").setAttribute("hidden", true);
	}
	deletePolygons();
	map.setZoom(zoom);
	map.setCenter(new google.maps.LatLng(center));
	load_polygons(JSON.parse(mapData.polygons));

	loadHistoricChart(JSON.parse(mapData.historic), JSON.parse(mapData.predictions));
}

//
// Header
//

function updateMapCart(id, val) {
	document.getElementById(id).innerHTML = val + " €";
}

function getStyleVariationPrice(val) {
	var classes = '';
	var innerHtml = val + " %"
	if (val > 0) {
		classes += 'text-success';
		innerHtml = '<i class="fa fa-arrow-up"></i>&ensp;' + innerHtml
	} else if (val < 0) {
		classes += 'text-warning';
		innerHtml = '<i class="fa fa-arrow-down"></i>&ensp;' + innerHtml
	}
	return [classes, innerHtml]
}

function updateMapCartPercentage(id, val) {
	var styleCard = getStyleVariationPrice(val)
	document.getElementById(id).innerHTML = styleCard[1];
	document.getElementById(id).className = 'h2 font-weight-bold mb-0 ' + styleCard[0];
}

function updateParentInfo(name, level) {
	const text = name + " | " + level;
	document.getElementById("parentName").innerHTML = text;
	document.getElementById("headerHistoricSales").innerHTML = text;
}


//
// Google maps
//

let map;
let infoWindow;
let polygons_loaded = [];
const default_center = { lat: 40.4667754, lng: -3.7037902 };
const default_zoom = 11;

function initMap() {
	const mapDiv = document.getElementById("map")
	map = new google.maps.Map(document.getElementById("map"), {
		center: default_center,
		zoom: default_zoom,
	});
	getAndSetMapData(1);
};

function load_polygons(polygons) {
	polygons.features.forEach(function (entry) {
		var coords_polygon = []
		entry.geometry.coordinates[0][0].forEach(function (coord) {
			var point = { lat: coord[1], lng: coord[0] }
			coords_polygon.push(point)
		})

		var geo_polygon_map = new google.maps.Polygon({
			paths: coords_polygon,
			strokeColor: entry.color,
			strokeOpacity: 0.8,
			strokeWeight: 3,
			fillColor: entry.color,
			fillOpacity: 0.20,
			title: entry.properties.name,
			price: entry.price,
			monthlyVariation: entry.monthly_variation,
			quarterlyVariation: entry.quarterly_variation,
			annualVariation: entry.annual_variation,
			geo_level: entry.level,
			best_moment_price: entry.best_moment_price,
			best_moment_date: entry.best_moment_date
		});

		if (entry.properties.level == 2) {
			geo_polygon_map.addListener("click", () => {
				getAndSetMapData(entry.properties.pk);
			});
		}
		geo_polygon_map.addListener("rightclick", showGeoData);
		polygons_loaded.push(geo_polygon_map)
		infoWindow = new google.maps.InfoWindow();
	});

	setMapOnAll(map);
}

function showGeoData(event) {
	var monthlyVariationStyle = getStyleVariationPrice(this.monthlyVariation);
	var quarterlyVariationStyle = getStyleVariationPrice(this.quarterlyVariation);
	var annualVariationStyle = getStyleVariationPrice(this.annualVariation);

	var contentString = "<b style='font-weight: 900;'>" + this.geo_level + " &nbsp; &nbsp;</b><br>" +
		"<b>" + this.title + "</b><br>";

	if (this.price) {
		contentString += "<b><strong>Precio actual:&ensp;</strong>" + this.price + " €</b><br>" +
			'<b><strong>Variaciones:</strong></b><br>' +
			'<b><strong>&ensp;Mensual:&ensp;</strong></b><b class="' + monthlyVariationStyle[0] + '">' + monthlyVariationStyle[1] + "</b></br>" +
			'<b><strong>&ensp;Trimestral:&ensp;</strong></b><b class="' + quarterlyVariationStyle[0] + '">' + quarterlyVariationStyle[1] + "</b></br>" +
			'<b><strong>&ensp;Anual:&ensp;</strong></b><b class="' + annualVariationStyle[0] + '">' + annualVariationStyle[1] + "</b></br>";
	} else {
		contentString += "<b> No Data </b>"
	}
	if (this.geo_level == "Distrito") {
		if (this.best_moment_price) {
			var bestMomentVariation = getStyleVariationPrice(Number(this.best_moment_price / this.price * 100 - 100).toFixed(2));
			contentString = contentString +
				'<b><strong>Mejor momento:&ensp;</strong></b><b>' + this.best_moment_date.substring(0, 7) + "</b></br>" +
				'<b><strong>&ensp;Precio máximo estimado:&ensp;</strong></b><b>' + this.best_moment_price + " €</b></br>" +
				'<b><strong>&ensp;Varción estimada:&ensp;</strong></b><b class="' + bestMomentVariation[0] + '">' + bestMomentVariation[1] + "</b></br>";
		} else {
			contentString = contentString +
				'<b><strong>Mejor momento:&ensp;</strong></b><b>Ahora</b></br>'
		}
	}

	// Replace the info window's content and position.
	infoWindow.setContent(contentString);
	infoWindow.setPosition(event.latLng);

	infoWindow.open(map);
};


function setMapOnAll(map) {
	for (let i = 0; i < polygons_loaded.length; i++) {
		polygons_loaded[i].setMap(map);
	}
};


function clearPolygons() {
	setMapOnAll(null);
};


function deletePolygons() {
	clearPolygons();
	polygons_loaded = [];
};


//
// Wallet Dashboard
//
function getAndSetWallet(loadId) {
	$.ajax({
		url: '/get_wallet_data/',
		type: 'GET',
		data: {
			'accountId': 2,
			'loadId': loadId
		},
		dataType: 'json',
		success: function (data) {
			loadWalletData(data);
		},
		statusCode: {
			500: function () {
				alert("Se ha producido un error");
			}
		}
	});
}

function resetWalletDashboard(event) {
	getAndSetWallet(event.target.options[event.target.selectedIndex].getAttribute('id'))
}

function loadWalletData(walletData) {
	const mapDiv = document.getElementById("map")
	map = new google.maps.Map(document.getElementById("map"), {
		center: { lat: 40.4167754, lng: -3.7037902 },
		zoom: 13,
	});
	var len_properties = walletData.wallet.properties.length
	var int_formater = new Intl.NumberFormat()
	document.getElementById("walletName").innerHTML = walletData.wallet.load.name;
	document.getElementById("countPropertiesWallet").innerHTML = len_properties;
	document.getElementById("priceWalletBuyed").innerHTML = int_formater.format(Math.trunc(walletData.total_buyed_price)) + ' €';
	document.getElementById("priceWalletEstimated").innerHTML = int_formater.format(Math.trunc(walletData.total_estimated_price)) + ' €';
	updateMapCartPercentage("totalCostEffectiveness", Number(walletData.total_estimated_price / walletData.total_buyed_price * 100 - 100).toFixed(1));
	createSelectWallet(walletData.loads, walletData.wallet.load.id);
	loadPropertiesMap(walletData.wallet.properties);
	loadFutureEstimatedChart(walletData.wallet.future_estimations, walletData.total_buyed_price);
	createWalletGeoTable("neigborhoodWalletResume", "neighborhoods", walletData.wallet.geo_resume);
	createWalletGeoTable("districtWalletResume", "districts", walletData.wallet.geo_resume);
	createWalletPropertiesTable("propertiesWalletResume", walletData.wallet.properties);
}

function createSelectWallet(data, id_selected) {
	var walletSelector = document.getElementById('selectWallet');
	walletSelector.innerHTML = '';
	data.forEach(function (wallet) {
		var option = createDomElement('option', "btn btn-secondary btn-neutral", wallet.name, wallet.id, null);
		if (wallet.id == id_selected) {
			option.selected = true;
		}
		walletSelector.options.add(option);
	})
}

function loadFutureEstimatedChart(data, invested) {
	// Variables
	$('#evolutionWalletChart').remove();
	$('#container-evolutionWalletChart').append('<canvas id="evolutionWalletChart" class="chart-canvas"></canvas>');
	var $chart = $('#evolutionWalletChart');


	// Methods

	function init($chart) {
		var labels = []
		var prices = []
		var values_invested = []
		var values_p = []
		var values_p_low = []
		var values_p_up = []

		for (let i = 0; i < data.date.length; i++) {
			labels.push(data.date[i].substring(0, 7))
			values_p.push(Number(data.price[i]).toFixed(0))
			values_p_low.push(Number(data.conf_low[i]).toFixed(0))
			values_p_up.push(Number(data.conf_up[i]).toFixed(0))
			values_invested.push(Number(invested).toFixed(0))
			prices.push(data.price[i])
			prices.push(data.conf_low[i])
			prices.push(data.conf_up[i])
		}
		prices.push(invested)

		var total = 0;
		for (var i = 0; i < prices.length; i++) {
			total += prices[i];
		}
		var avg_prices = total / prices.length;

		var historicChart = new Chart($chart, {
			type: 'line',
			options: {
				scales: {
					yAxes: [{
						gridLines: {
							lineWidth: 1,
							color: Charts.colors.gray[900],
							zeroLineColor: Charts.colors.gray[900]
						},
						ticks: {
							callback: function (value) {
								if (!(value % 10)) {
									return '€' + new Intl.NumberFormat().format(value);
								}
							},
							min: Math.min.apply(this, prices) - avg_prices * 0.05,
							max: Math.max.apply(this, prices) + avg_prices * 0.05
						}
					}],
					xAxes: {
						type: 'time'
					}
				},
				legend: {
					display: true,
					position: 'top',
					labels: {
						fontColor: "#FFFFFF",
					},
					align: "end",
					labels: {
						filter: function (item, chart) {
							if (item.text == 'Cota Inferior' || item.text == 'Cota Superior') {
								return false;
							} else {
								return item;
							}
						}
					}
				},
				tooltips: {
					callbacks: {
						label: function (item, data) {
							var label = data.datasets[item.datasetIndex].label || '';
							var yLabel = item.yLabel;
							var content = '';

							if (data.datasets.length > 1) {
								content += label + '    ';
							}

							content += new Intl.NumberFormat().format(yLabel) + ' €';

							return content;
						}
					}
				}
			},
			data: {
				labels: labels,
				datasets: [{
					label: 'Capital Invertido',
					data: values_invested,
					borderColor: "rgb(192, 75, 75)",
					backgroundColor: "rgb(192, 75, 75)",
					fill: false,
					borderWidth: 3
				}, {
					label: 'Predicciones',
					data: values_p,
					borderColor: "rgb(75, 192, 192)",
					backgroundColor: "rgb(75, 192, 192)",
					fill: false,
					borderWidth: 2
				},
				{
					label: 'Cota Inferior',
					data: values_p_low,
					borderColor: "rgb(75, 192, 192)",
					backgroundColor: "rgb(75, 192, 192, .4)",
					fill: false,
					borderWidth: 0
				},
				{
					label: 'Cota Superior',
					data: values_p_up,
					borderColor: "rgb(75, 192, 192)",
					backgroundColor: "rgb(75, 192, 192, .4)",
					fill: 2,
					borderWidth: 0,
				}
				]
			}
		});

		// Save to jQuery object
		$chart.data('chart', historicChart);

	};


	// Events

	if ($chart.length) {
		init($chart);
	}

};


function loadPropertiesMap(properties) {
	properties.forEach(function (entry) {
		var costEffectiveness = entry.estimated_price / entry.buyed_price * 100 - 100;
		var icon = {};
		if (costEffectiveness >= 0) {
			icon = {
				url: "/static/assets/img/icons/maps/rsz_grn-blank.png",
				size: new google.maps.Size(32, 32),
				origin: new google.maps.Point(0, 0), // origin
				anchor: new google.maps.Point(16, 32) // anchor
			}
		} else {
			icon = {
				url: "/static/assets/img/icons/maps/rsz_red-blank.png",
				size: new google.maps.Size(32, 32),
				origin: new google.maps.Point(0, 0), // origin
				anchor: new google.maps.Point(16, 32) // anchor
			}
		}

		var marker = new google.maps.Marker({
			position: new google.maps.LatLng(entry.geo.location.latitude, entry.geo.location.longitude),
			map,
			//animation: google.maps.Animation.DROP,
			icon: icon,
			optimized: true,
			builded_surface: entry.cadastre.builded_surface,
			year_built: entry.cadastre.year_built,
			cadastral_reference: entry.cadastre.cadastral_reference,
			latLng: new google.maps.Point(entry.geo.location.latitude, entry.geo.location.longitude),
			buyed_price: entry.buyed_price,
			estimated_price: entry.estimated_price,
			costEffectiveness: costEffectiveness,
			best_moment: entry.best_moment ? entry.best_moment : null
		});
		marker.addListener("click", showPropertyData);
		infoWindow = new google.maps.InfoWindow();
	});
}

function showPropertyData(event) {
	var intFormater = new Intl.NumberFormat()
	var costEffectivenessStyle = getStyleVariationPrice(Number(this.costEffectiveness).toFixed(2));
	var contentString = "<b style='font-weight: 900;'>" + this.cadastral_reference + " &nbsp; &nbsp;</b><br>" +
		'<b><strong>Año contrucción:&ensp;</strong></b><b>' + this.year_built + "</b></br>" +
		'<b><strong>Metros cuadrados:&ensp;</strong></b><b>' + this.builded_surface + "</b></br>" +
		'<b><strong>Precio compra:&ensp;</strong></b><b>' + intFormater.format(this.buyed_price) + "</b></br>" +
		'<b><strong>Precio estimado:&ensp;</strong></b><b>' + intFormater.format(this.estimated_price) + "</b></br>" +
		'<b><strong>Rentabilidad esperada:&ensp;</strong></b><b class="' + costEffectivenessStyle[0] + '">' + costEffectivenessStyle[1] + "</b></br>"
	if (this.best_moment) {
		var costEffectivenessStyle = getStyleVariationPrice(Number(this.best_moment.estimated_price / this.buyed_price * 100 - 100).toFixed(2));
		contentString = contentString +
			'<b><strong>Mejor momento:&ensp;</strong></b><b>' + this.best_moment.date.substring(0, 7) + "</b></br>" +
			'<b><strong>&ensp;Precio máximo estimado:&ensp;</strong></b><b>' + intFormater.format(this.best_moment.estimated_price) + "</b></br>" +
			'<b><strong>&ensp;Rentabilida máxima esperada:&ensp;</strong></b><b class="' + costEffectivenessStyle[0] + '">' + costEffectivenessStyle[1] + "</b></br>";
	} else {
		contentString = contentString +
			'<b><strong>Mejor momento:&ensp;</strong></b><b>Ahora</b></br>'
	}

	infoWindow.setContent(contentString);
	infoWindow.setPosition(event.latLng);

	infoWindow.open(map);
}

function createWalletGeoTable(idTable, geoKey, data) {
	var intFormater = new Intl.NumberFormat()
	var table = document.getElementById(idTable);
	table.querySelectorAll('tbody tr:nth-child(n+1)').forEach(tr => tr.remove())
	for (const [geoName, value] of Object.entries(data[geoKey])) {
		var tr = createDomElement('tr');

		var costEffectivenessStyle = getStyleVariationPrice(Number(value.total_estimated / value.total_buyed * 100 - 100).toFixed(1));
		var tdName = createDomElement('td', null, geoName);
		var tdCount = createDomElement('td', null, value.total_properties);
		var tdBuyed = createDomElement('td', null, intFormater.format(value.total_buyed.toFixed(0)));
		var tdEstimated = createDomElement('td', null, intFormater.format(value.total_estimated.toFixed(0)));
		var tdCostEffectiveness = createDomElement('td', costEffectivenessStyle[0], costEffectivenessStyle[1]);

		tr.appendChild(tdName);
		tr.appendChild(tdCount);
		tr.appendChild(tdBuyed);
		tr.appendChild(tdEstimated);
		tr.appendChild(tdCostEffectiveness);

		$(table).find('tbody').append(tr);
	}

	var rows = Array.from(table.querySelectorAll('tbody tr:nth-child(n+1)'));
	loadGeoResumeChart(idTable + 'Chart', rows);
}

function createWalletPropertiesTable(idTable, properties) {
	var intFormater = new Intl.NumberFormat()
	var table = document.getElementById(idTable);
	table.querySelectorAll('tbody tr:nth-child(n+1)').forEach(tr => tr.remove())
	properties.forEach(function (entry) {
		var tr = createDomElement('tr');

		var costEffectivenessStyle = getStyleVariationPrice(Number(entry.estimated_price / entry.buyed_price * 100 - 100).toFixed(1));
		var tdRc = createDomElement('td', null, entry.cadastre.cadastral_reference);
		var tdSurface = createDomElement('td', null, entry.cadastre.builded_surface);
		var tdYear = createDomElement('td', null, entry.cadastre.year_built);
		var tdBuyed = createDomElement('td', null, intFormater.format(entry.buyed_price.toFixed(0)));
		var tdEstimated = createDomElement('td', null, intFormater.format(entry.estimated_price.toFixed(0)));
		var tdCostEffectiveness = createDomElement('td', costEffectivenessStyle[0], costEffectivenessStyle[1]);
		if (entry.best_moment) {
			costEffectivenessStyle = getStyleVariationPrice(Number(entry.best_moment.estimated_price / entry.buyed_price * 100 - 100).toFixed(2));
			var tdBestMoment = createDomElement('td', null, entry.best_moment.date.substring(0, 7));
			var tdEstimatedMax = createDomElement('td', null, intFormater.format(entry.best_moment.estimated_price));
			var tdCostEffectivenessMax = createDomElement('td', costEffectivenessStyle[0], costEffectivenessStyle[1]);
		} else {
			var tdBestMoment = createDomElement('td', null, "2021-04 (Ahora)");
			var tdEstimatedMax = createDomElement('td', null, intFormater.format(entry.estimated_price.toFixed(0)));
			var tdCostEffectivenessMax = createDomElement('td', costEffectivenessStyle[0], costEffectivenessStyle[1]);
		}

		tr.appendChild(tdRc);
		tr.appendChild(tdSurface);
		tr.appendChild(tdYear);
		tr.appendChild(tdBuyed);
		tr.appendChild(tdEstimated);
		tr.appendChild(tdCostEffectiveness);
		tr.appendChild(tdBestMoment);
		tr.appendChild(tdEstimatedMax);
		tr.appendChild(tdCostEffectivenessMax);

		$(table).find('tbody').append(tr);
	});

	var rows = Array.from(table.querySelectorAll('tbody tr:nth-child(n+1)'));
	loadGeoResumeChart(idTable + 'Chart', rows);
}

function isNumeric(str) {
	if (typeof str != "string") return false
	return !isNaN(str) &&
		!isNaN(parseFloat(str))
}

const getCellValue = function (tr, idx) { return tr.children[idx].innerText || tr.children[idx].textContent; }

const comparer = function (idx, asc) {
	return function (a, b) {
		return function (v1, v2) {
			if (v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2)) {
				return v1 - v2
			} else if (isNumeric(v1.replace(/,/g, "").replace('%', "").replace(/\./g, "")) && isNumeric(v2.replace(/,/g, "").replace('%', "").replace(/\./g, ""))) {
				return parseInt(v1.replace(/,/g, "").replace('%', "").replace(/\./g, "")) > parseInt(v2.replace(/,/g, "").replace('%', "").replace(/\./g, "")) ? 1 : -1
			} else {
				return v1.toString().localeCompare(v2)
			}
		}(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));
	}
};

document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
	const table = th.closest("table");
	Array.from(table.querySelectorAll('tbody tr:nth-child(n+1)'))
		.sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
		.forEach(tr => $(table).find('tbody').append(tr));

	var rows = Array.from(table.querySelectorAll('tbody tr:nth-child(n+1)'));
	loadGeoResumeChart(table.id + 'Chart', rows);
})));

function loadGeoResumeChart(idChart, data, maxColumns = 21) {

	// Variables
	$('#' + idChart).remove();
	$('#container-' + idChart).append('<canvas id="' + idChart + '" class="chart-canvas"></canvas>');
	var $chart = $('#' + idChart);


	// Methods

	function init($chart) {
		var labels = [];
		var values_estimated = [];
		var values_buyed = [];
		var intFormater = new Intl.NumberFormat();
		var i = 0;
		var BreakException = {};

		try {
			data.forEach(function (row) {
				labels.push(row.cells[0].innerHTML);
				values_buyed.push(parseInt(row.cells[2].innerHTML.replace(/,/g, "").replace(/\./g, "")));
				values_estimated.push(parseInt(row.cells[3].innerHTML.replace(/,/g, "").replace(/\./g, "")));
				i = i + 1;
				if (i == maxColumns) {
					throw BreakException; // Mejor opción para interrumpir
				}
			});
		} catch (e) {
			if (e !== BreakException) throw e;
		}

		var geoResumeChart = new Chart($chart, {
			type: 'bar',
			options: {
				pointStyle: 'rect',
				legend: {
					display: true,
					position: 'top',
					labels: {
						fontColor: "#FFFFFF",
					},
					align: "end",
					borderWidth: 1,
				},
				tooltips: {
					callbacks: {
						label: function (item, data) {
							var label = data.datasets[item.datasetIndex].label || '';
							var yLabel = item.yLabel;
							var content = '';

							if (data.datasets.length > 1) {
								content += label + '    ';
							}

							content += intFormater.format(yLabel) + ' €';
							// content += yLabel + ' €';

							return content;
						}
					}
				}
			},
			data: {
				labels: labels,
				datasets: [{
					label: 'Invertido',
					data: values_buyed,
					borderColor: "rgb(54, 162, 235)",
					backgroundColor: "rgb(54, 162, 235)",
					barThickness: 12,
					pointStyle: 'rect'
				}, {
					label: 'Estimado',
					data: values_estimated,
					borderColor: "rgb(75, 192, 192)",
					backgroundColor: "rgb(75, 192, 192)",
					barThickness: 12,
					pointStyle: 'rect'
				}]
			}
		});

		// Save to jQuery object
		$chart.data('chart', geoResumeChart);

	};


	// Events

	if ($chart.length) {
		init($chart);
	}

};

//
// Bars chart
//

var BarsChart = (function () {

	//
	// Variables
	//

	var $chart = $('#chart-bars');


	//
	// Methods
	//

	// Init chart
	function initChart($chart) {

		// Create chart
		var ordersChart = new Chart($chart, {
			type: 'bar',
			data: {
				labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
				datasets: [{
					label: 'Sales',
					data: [25, 20, 30, 22, 17, 29]
				}]
			}
		});

		// Save to jQuery object
		$chart.data('chart', ordersChart);
	}


	// Init chart
	if ($chart.length) {
		initChart($chart);
	}

})();

'use strict';

//
// Historic chart
//

function loadHistoricChart(historic, predictions) {

	// Variables
	$('#chart-historic-dark').remove();
	$('#container-chart-historic-dark').append('<canvas id="chart-historic-dark" class="chart-canvas"></canvas>');
	var $chart = $('#chart-historic-dark');


	// Methods

	function init($chart) {
		var labels = []
		var prices = []
		var values_c = []
		var values_p = []
		var values_p_low = []
		var values_p_up = []

		historic.forEach(function (hist) {
			labels.push(hist.fields.date.substring(0, 7))
			values_c.push(hist.fields.price)
			if (hist.fields.price) {
				prices.push(hist.fields.price)
			}
		})

		values_p = new Array(values_c.length)
		values_p_low = new Array(values_c.length)
		values_p_up = new Array(values_c.length)

		predictions.forEach(function (pred) {
			labels.push(pred.fields.date.substring(0, 7))
			values_p.push(Number(pred.fields.price).toFixed(0))
			values_p_low.push(Number(pred.fields.conf_low).toFixed(0))
			values_p_up.push(Number(pred.fields.conf_up).toFixed(0))
			prices.push(pred.fields.price)
		})

		var historicChart = new Chart($chart, {
			type: 'line',
			options: {
				scales: {
					yAxes: [{
						gridLines: {
							lineWidth: 1,
							color: Charts.colors.gray[900],
							zeroLineColor: Charts.colors.gray[900]
						},
						ticks: {
							callback: function (value) {
								if (!(value % 10)) {
									return '€' + value;
								}
							},
							min: Math.min.apply(this, prices) - 500,
							max: Math.max.apply(this, prices) + 500
						}
					}],
					xAxes: {
						type: 'time'
					}
				},
				legend: {
					display: true,
					position: 'top',
					labels: {
						fontColor: "#FFFFFF",
					},
					align: "end",
					labels: {
						filter: function (item, chart) {
							if (item.text == 'Cota Inferior' || item.text == 'Cota Superior') {
								return false;
							} else {
								return item;
							}
						}
					}
				},
				tooltips: {
					callbacks: {
						label: function (item, data) {
							var label = data.datasets[item.datasetIndex].label || '';
							var yLabel = item.yLabel;
							var content = '';

							if (data.datasets.length > 1) {
								content += label + '    ';
							}

							content += yLabel + ' €';

							return content;
						}
					}
				}
			},
			data: {
				labels: labels,
				datasets: [{
					label: 'Actuales',
					data: values_c,
					borderColor: "rgb(54, 162, 235)",
					backgroundColor: "rgb(54, 162, 235)",
					fill: false,
				}, {
					label: 'Predicciones',
					data: values_p,
					borderColor: "rgb(75, 192, 192)",
					backgroundColor: "rgb(75, 192, 192)",
					fill: false,
					borderWidth: 0.7
				},
				{
					label: 'Cota Inferior',
					data: values_p_low,
					borderColor: "rgb(75, 192, 192)",
					backgroundColor: "rgb(75, 192, 192, .4)",
					fill: false,
					borderWidth: 0
				},
				{
					label: 'Cota Superior',
					data: values_p_up,
					borderColor: "rgb(75, 192, 192)",
					backgroundColor: "rgb(75, 192, 192, .4)",
					fill: 2,
					borderWidth: 0,
				}
				]
			}
		});

		// Save to jQuery object
		$chart.data('chart', historicChart);

	};


	// Events

	if ($chart.length) {
		init($chart);
	}

};

//
// Bootstrap Datepicker
//

'use strict';

var Datepicker = (function () {

	// Variables

	var $datepicker = $('.datepicker');


	// Methods

	function init($this) {
		var options = {
			disableTouchKeyboard: true,
			autoclose: false
		};

		$this.datepicker(options);
	}


	// Events

	if ($datepicker.length) {
		$datepicker.each(function () {
			init($(this));
		});
	}

})();

//
// Form control
//

'use strict';

var noUiSlider = (function () {

	// Variables

	// var $sliderContainer = $('.input-slider-container'),
	// 		$slider = $('.input-slider'),
	// 		$sliderId = $slider.attr('id'),
	// 		$sliderMinValue = $slider.data('range-value-min');
	// 		$sliderMaxValue = $slider.data('range-value-max');;


	// // Methods
	//
	// function init($this) {
	// 	$this.on('focus blur', function(e) {
	//       $this.parents('.form-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
	//   }).trigger('blur');
	// }
	//
	//
	// // Events
	//
	// if ($input.length) {
	// 	init($input);
	// }



	if ($(".input-slider-container")[0]) {
		$('.input-slider-container').each(function () {

			var slider = $(this).find('.input-slider');
			var sliderId = slider.attr('id');
			var minValue = slider.data('range-value-min');
			var maxValue = slider.data('range-value-max');

			var sliderValue = $(this).find('.range-slider-value');
			var sliderValueId = sliderValue.attr('id');
			var startValue = sliderValue.data('range-value-low');

			var c = document.getElementById(sliderId),
				d = document.getElementById(sliderValueId);

			noUiSlider.create(c, {
				start: [parseInt(startValue)],
				connect: [true, false],
				//step: 1000,
				range: {
					'min': [parseInt(minValue)],
					'max': [parseInt(maxValue)]
				}
			});

			c.noUiSlider.on('update', function (a, b) {
				d.textContent = a[b];
			});
		})
	}

	if ($("#input-slider-range")[0]) {
		var c = document.getElementById("input-slider-range"),
			d = document.getElementById("input-slider-range-value-low"),
			e = document.getElementById("input-slider-range-value-high"),
			f = [d, e];

		noUiSlider.create(c, {
			start: [parseInt(d.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
			connect: !0,
			range: {
				min: parseInt(c.getAttribute('data-range-value-min')),
				max: parseInt(c.getAttribute('data-range-value-max'))
			}
		}), c.noUiSlider.on("update", function (a, b) {
			f[b].textContent = a[b]
		})
	}

})();

//
// Scrollbar
//

'use strict';

var Scrollbar = (function () {

	// Variables

	var $scrollbar = $('.scrollbar-inner');


	// Methods

	function init() {
		$scrollbar.scrollbar().scrollLock()
	}


	// Events

	if ($scrollbar.length) {
		init();
	}

})();


function autocomplete(inp, arr) {
	/*the autocomplete function takes two arguments,
	the text field element and an array of possible autocompleted values:*/
	var currentFocus;
	/*execute a function when someone writes in the text field:*/
	inp.addEventListener("input", function (e) {
		var a, b, i, val = this.value;
		/*close any already open lists of autocompleted values*/
		closeAllLists();
		if (!val) { return false; }
		currentFocus = -1;
		/*create a DIV element that will contain the items (values):*/
		a = document.createElement("DIV");
		a.setAttribute("id", this.id + "autocomplete-list");
		a.setAttribute("class", "autocomplete-items");
		/*append the DIV element as a child of the autocomplete container:*/
		this.parentNode.appendChild(a);
		var count = 0;
		/*for each item in the array...*/
		for (i = 0; i < arr.length; i++) {
			/*check if the item starts with the same letters as the text field value:*/
			if (arr[i].fields.name.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
				/*create a DIV element for each matching element:*/
				b = document.createElement("DIV");
				/*make the matching letters bold:*/
				b.innerHTML = "<strong>" + arr[i].fields.name.substr(0, val.length) + "</strong>";
				b.innerHTML += arr[i].fields.name.substr(val.length);
				/*insert a input field that will hold the current array item's value:*/
				b.innerHTML += "<input type='hidden' pk=" + arr[i].pk + " value='" + arr[i].fields.name + "'>";
				/*execute a function when someone clicks on the item value (DIV element):*/
				b.addEventListener("click", function (e) {
					/*insert the value for the autocomplete text field:*/
					inp.value = this.getElementsByTagName("input")[0].value;
					document.getElementById("road").value = this.getElementsByTagName("input")[0].getAttribute("pk")
					/*close the list of autocompleted values,
					(or any other open lists of autocompleted values:*/
					closeAllLists();
				});
				a.appendChild(b);
				count = count + 1;
			}
			if (count == 5) { break; }
		}
	});
	/*execute a function presses a key on the keyboard:*/
	inp.addEventListener("keydown", function (e) {
		var x = document.getElementById(this.id + "autocomplete-list");
		if (x) x = x.getElementsByTagName("div");
		if (e.keyCode == 40) {
			/*If the arrow DOWN key is pressed,
			increase the currentFocus variable:*/
			currentFocus++;
			/*and and make the current item more visible:*/
			addActive(x);
		} else if (e.keyCode == 38) { //up
			/*If the arrow UP key is pressed,
			decrease the currentFocus variable:*/
			currentFocus--;
			/*and and make the current item more visible:*/
			addActive(x);
		} else if (e.keyCode == 13) {
			/*If the ENTER key is pressed, prevent the form from being submitted,*/
			e.preventDefault();
			if (currentFocus > -1) {
				/*and simulate a click on the "active" item:*/
				if (x) x[currentFocus].click();
			}
		}
	});
	function addActive(x) {
		/*a function to classify an item as "active":*/
		if (!x) return false;
		/*start by removing the "active" class on all items:*/
		removeActive(x);
		if (currentFocus >= x.length) currentFocus = 0;
		if (currentFocus < 0) currentFocus = (x.length - 1);
		/*add class "autocomplete-active":*/
		x[currentFocus].classList.add("autocomplete-active");
	}
	function removeActive(x) {
		/*a function to remove the "active" class from all autocomplete items:*/
		for (var i = 0; i < x.length; i++) {
			x[i].classList.remove("autocomplete-active");
		}
	}
	function closeAllLists(elmnt) {
		/*close all autocomplete lists in the document,
		except the one passed as an argument:*/
		var x = document.getElementsByClassName("autocomplete-items");
		for (var i = 0; i < x.length; i++) {
			if (elmnt != x[i] && elmnt != inp) {
				x[i].parentNode.removeChild(x[i]);
			}
		}
	}
	/*execute a function when someone clicks in the document:*/
	document.addEventListener("click", function (e) {
		closeAllLists(e.target);
	});
}
