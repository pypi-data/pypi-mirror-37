var MS2_PLUGINS = {
	"desktop": [ {
		"name": "Map",
		"cfg": {
			"tools": ["locate", "measurement", "draw"],
			"mapOptions": {
				"openlayers": {
					"interactions": {
						"pinchRotate": false,
						"altShiftDragRotate": false
					}
				},
				"leaflet": {
					"attribution": {
						"container": "#mapstore-map-footer-container"
					}
				}
			}
		}
	}, {
		"name": "DrawerMenu"
	}, {
		"name": "BackgroundSelector",
		"cfg": {
			"style": { "bottom": 0, "marginBottom": 30 },
			"dimensions": {
				"side": 65,
				"sidePreview": 65,
				"frame": 3,
				"margin": 5,
				"label": false,
				"vertical": false
			}
		}
	},
	{
		"name": "Identify",
		"cfg": {
			"showFullscreen": false,
			"dock": true,
			"position": "right",
			"size": 0.5,
			"fluid": true,
			"viewerOptions": {
				"container": "{context.ReactSwipe}"
			}
		},
		"override": {
			"Toolbar": {
				"position": 11,
				"alwaysVisible": false
			}
		}
	}, {
		"name": "ZoomAll",
		"override": {
			"Toolbar": {
				"alwaysVisible": false
			}
		}
	}, {
		"name": "FeatureEditor",
		"cfg": {
			"editingAllowedRoles": ["NONE"],
			"canEdit": false
		}
	},{
		"name": "QueryPanel",
		"cfg": {
			"activateQueryTool": true,
			"spatialOperations": [
				{"id": "INTERSECTS", "name": "queryform.spatialfilter.operations.intersects"},
				{"id": "BBOX", "name": "queryform.spatialfilter.operations.bbox"},
				{"id": "CONTAINS", "name": "queryform.spatialfilter.operations.contains"},
				{"id": "WITHIN", "name": "queryform.spatialfilter.operations.within"}
			],
			"spatialMethodOptions": [
				{"id": "Viewport", "name": "queryform.spatialfilter.methods.viewport"},
				{"id": "BBOX", "name": "queryform.spatialfilter.methods.box"},
				{"id": "Circle", "name": "queryform.spatialfilter.methods.circle"},
				{"id": "Polygon", "name": "queryform.spatialfilter.methods.poly"}
			]
		}
	  },{
		"name": "TOC",
		"cfg": {
			"activateQueryTool": true,
			"activateAddLayerButton": true,
			"activateMetedataTool": false,
			"activateSettingsTool": false,
			"activateRemoveLayer": false,
			"spatialOperations": [
				{ "id": "INTERSECTS", "name": "queryform.spatialfilter.operations.intersects" },
				{ "id": "BBOX", "name": "queryform.spatialfilter.operations.bbox" },
				{ "id": "CONTAINS", "name": "queryform.spatialfilter.operations.contains" },
				{ "id": "WITHIN", "name": "queryform.spatialfilter.operations.within" }
			],
			"spatialMethodOptions": [
				{ "id": "Viewport", "name": "queryform.spatialfilter.methods.viewport" },
				{ "id": "BBOX", "name": "queryform.spatialfilter.methods.box" },
				{ "id": "Circle", "name": "queryform.spatialfilter.methods.circle" },
				{ "id": "Polygon", "name": "queryform.spatialfilter.methods.poly" }
			]
		}

	}, {
		"name": "MetadataExplorer",
		"cfg": {
			"wrap": true
		}
	}, {
		"name": "Toolbar",
		"id": "NavigationBar",
		"cfg": {
			"id": "navigationBar",
			"layout": "horizontal"
		}
	}, {
		"name": "MapLoading",
		"override": {
			"Toolbar": {
				"alwaysVisible": true
			}
		}
	}, "Cookie",
		"OmniBar", {
		"name": "GoFull",
		"override": {
			"Toolbar": {
				"alwaysVisible": false
			}
		}
	},
		"Expander", "ScaleBox", "Undo", "Redo",
	{
		"name": "FullScreen",
		"override": {
			"Toolbar": {
				"alwaysVisible": false
			}
		}
	}, "BurgerMenu", "MapFooter", {
		"name": "Print",
		"cfg": {
			"useFixedScales": true
		}
	},
	{
		"name": "ZoomIn",
		"override": {
			"Toolbar": {
				"alwaysVisible": true
			}
		}
	}, {
		"name": "Measure"
	}, {
		"name": "ZoomOut",
		"override": {
			"Toolbar": {
				"alwaysVisible": true
			}
		}
	}, "Widgets", "SaveAs", "Notifications"
	]
}
