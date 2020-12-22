# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.2.0
# December 21, 2020
# ----------------------------------------------

import ScriptEnv

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.NewProject()
oProject.InsertDesign("Maxwell 2D", "Maxwell2DDesign1", "DCConduction", "")
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")

oEditor.CreateRectangle(
    [
        "NAME:RectangleParameters",
        "IsCovered:=", True,
        "XStart:=", "0.1mm",
        "YStart:=", "0mm",
        "ZStart:=", "0mm",
        "Width:=", "100mm",
        "Height:=", "10mm",
        "WhichAxis:=", "Z"
    ],

    [
        "NAME:Attributes",
        "Name:=", "Rectangle1",
        "Flags:=", "",
        "Color:=", "(143 175 143)",
        "Transparency:=", 0,
        "PartCoordinateSystem:=", "Global",
        "UDMId:=", "",
        "MaterialValue:=", "\"vacuum\"",
        "SurfaceMaterialValue:=", "\"\"",
        "SolveInside:=", False,
        "ShellElement:=", False,
        "ShellElementThickness:=", "0mm",
        "IsMaterialEditable:=", True,
        "UseMaterialAppearance:=", False,
        "IsLightweight:=", False
    ])

oDesign.ChangeProperty(
    [
        "NAME:AllTabs",
        [
            "NAME:LocalVariableTab",
            [
                "NAME:PropServers",
                "LocalVariables"
            ],

            [
                "NAME:NewProps",
                [
                    "NAME:a1",
                    "PropType:=", "VariableProp",
                    "UserDef:=", True,
                    "Value:=", "100mm"
                ]
            ]
        ]
    ])

oEditor.ChangeProperty(
    [
        "NAME:AllTabs",
        [
            "NAME:Geometry3DCmdTab",
            [
                "NAME:PropServers",
                "Rectangle1:CreateRectangle:1"
            ],

            [
                "NAME:ChangedProps",
                [
                    "NAME:XSize",
                    "Value:=", "a1"
                ]
            ]
        ]
    ])

oDesign.ChangeProperty(
    [
        "NAME:AllTabs",
        [
            "NAME:LocalVariableTab",
            [
                "NAME:PropServers",
                "LocalVariables"
            ],

            [
                "NAME:NewProps",
                [
                    "NAME:b1",
                    "PropType:=", "VariableProp",
                    "UserDef:=", True,
                    "Value:=", "10mm"
                ]
            ]
        ]
    ])

oEditor.ChangeProperty(
    [
        "NAME:AllTabs",
        [
            "NAME:Geometry3DCmdTab",
            [
                "NAME:PropServers",
                "Rectangle1:CreateRectangle:1"
            ],

            [
                "NAME:ChangedProps",
                [
                    "NAME:YSize",
                    "Value:=", "b1"
                ]
            ]
        ]
    ])

oEditor.AssignMaterial(

    [
        "NAME:Selections",
        "AllowRegionDependentPartSelectionForPMLCreation:=", True,
        "AllowRegionSelectionForPMLCreation:=", True,
        "Selections:=", "Rectangle1"
    ],

    [
        "NAME:Attributes",
        "MaterialValue:=", "\"copper\"",
        "SolveInside:=", True,
        "ShellElement:=", False,
        "ShellElementThickness:=", "nan ",
        "IsMaterialEditable:=", True,
        "UseMaterialAppearance:=", False,
        "IsLightweight:=", False

    ])

oEditor.ChangeProperty(

    [

        "NAME:AllTabs",
        [
            "NAME:Geometry3DAttributeTab",
            [
                "NAME:PropServers",
                "Rectangle1"
            ],
            [
                "NAME:ChangedProps",
                [
                    "NAME:Color",
                    "R:=", 255,
                    "G:=", 128,
                    "B:=", 64
                ]
            ]
        ]
    ])
oEditor.ChangeProperty(
    [
        "NAME:AllTabs",
        [
            "NAME:Geometry3DAttributeTab",
            [
                "NAME:PropServers",
                "Rectangle1"
            ],
            [
                "NAME:ChangedProps",
                [
                    "NAME:Transparent",
                    "Value:=", 0.6
                ]
            ]
        ]
    ])

oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignVoltage(
    [
        "NAME:Voltage1",
        "Edges:=", [10],
        "Value:=", "0V",
        "CoordinateSystem:=", ""
    ])

oModule.AssignVoltage(
    [
        "NAME:Voltage2",
        "Edges:=", [8],
        "Value:=", "24V",
        "CoordinateSystem:=", ""
    ])

oModule = oDesign.GetModule("AnalysisSetup")

oModule.InsertSetup("DCConduction",
                    [
                        "NAME:Setup1",
                        "Enabled:=", True,

                        [
                            "NAME:MeshLink",
                            "ImportMesh:=", False

                        ],

                        "MaximumPasses:=", 10,
                        "MinimumPasses:=", 2,
                        "MinimumConvergedPasses:=", 1,
                        "PercentRefinement:=", 30,
                        "SolveFieldOnly:=", False,
                        "PercentError:=", 0.5,
                        "SolveMatrixAtLast:=", True,
                        "NonLinearResidual:=", 0.001

                    ])

oDesign.AnalyzeAll()
oModule = oDesign.GetModule("FieldsReporter")
oModule.CreateFieldPlot(

    [
        "NAME:Mag_J1",
        "SolutionName:=", "Setup1 : LastAdaptive",
        "UserSpecifyName:=", 0,
        "UserSpecifyFolder:=", 0,
        "QuantityName:=", "Mag_J",
        "PlotFolder:=", "J",
        "StreamlinePlot:=", False,
        "AdjacentSidePlot:=", False,
        "FullModelPlot:=", False,
        "IntrinsicVar:=", "",
        "PlotGeomInfo:=", [1, "Surface", "FacesList", 1, "6"],
        "FilterBoxes:=", [0],

        [
            "NAME:PlotOnSurfaceSettings",
            "Filled:=", False,
            "IsoValType:=", "Fringe",
            "AddGrid:=", False,
            "MapTransparency:=", True,
            "Refinement:=", 0,
            "Transparency:=", 0,
            "SmoothingLevel:=", 0,
            "ShadingType:=", 0,

            [

                "NAME:Arrow3DSpacingSettings",
                "ArrowUniform:=", True,
                "ArrowSpacing:=", 0,
                "MinArrowSpacing:=", 0,
                "MaxArrowSpacing:=", 0

            ],

            "GridColor:=", [255, 255, 255]

        ],

        "EnableGaussianSmoothing:=", False

    ], "Field")

oDesign.ChangeProperty(
    [

        "NAME:AllTabs",
        [
            "NAME:LocalVariableTab",
            [
                "NAME:PropServers",
                "LocalVariables"
            ],

            [
                "NAME:ChangedProps",
                [
                    "NAME:b1",
                    "Value:=", "25mm"
                ]
            ]
        ]
    ])

oDesign.Undo()

oProject.Save()
