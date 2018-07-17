/*
 * elstat.java
 */

import com.comsol.model.*;
import com.comsol.model.util.*;
import java.io.FileReader;
import java.io.IOException;
import java.io.BufferedReader;


/** Model exported on Jan 24 2018, 15:04 by COMSOL 5.3.0.316. */
public class elstat {

	public static Model run() throws IOException{		
		String[] pole = new String[2];
		FileReader input = new FileReader("./tests/parameters.txt");
		BufferedReader bufRead = new BufferedReader(input);
		String myLine = null;
		int j = 0;		
		myLine = bufRead.readLine(); // read values separated by gaps
		String[] array2 = myLine.split(" ");			
		input.close();		
		Model model = ModelUtil.create("Model");
		model.modelPath("./tests");

		model.label("elstat.mph");

		model.comments("Untitled\n\n");

		model.param().set("a", array2[0]);
		model.param().set("b", array2[1]);


		model.component().create("comp1", true);

		model.component("comp1").geom().create("geom1", 2);

		model.result().table().create("tbl1", "Table");

		model.component("comp1").mesh().create("mesh1");

		model.component("comp1").geom("geom1").create("r1", "Rectangle");
		model.component("comp1").geom("geom1").feature("r1").set("pos", new double[]{-0.75, -0.1});
		model.component("comp1").geom("geom1").feature("r1").set("size", new String[]{"a", "b"});
		model.component("comp1").geom("geom1").run();

		model.variable().create("var1");

		model.component("comp1").material().create("mat1", "Common");
		model.component("comp1").material("mat1").info().create("Composition");
		model.component("comp1").material("mat1").propertyGroup("def").func().create("k", "Piecewise");
		model.component("comp1").material("mat1").propertyGroup("def").func().create("C", "Piecewise");
		model.component("comp1").material("mat1").propertyGroup("def").func().create("rho_gas_2", "Piecewise");
		model.component("comp1").material("mat1").propertyGroup("def").func().create("TD", "Piecewise");
		model.component("comp1").material("mat1").propertyGroup("def").func().create("eta", "Piecewise");

		model.component("comp1").physics().create("es", "Electrostatics", "geom1");
		model.component("comp1").physics("es").create("gnd1", "Ground", 1);
		model.component("comp1").physics("es").feature("gnd1").selection().set(new int[]{4});
		model.component("comp1").physics("es").create("sfcd1", "SurfaceChargeDensity", 1);
		model.component("comp1").physics("es").feature("sfcd1").selection().set(new int[]{1});

		model.result().table("tbl1").comments("Line Maximum 1 ()");

		model.component("comp1").view("view1").axis().set("xmin", -0.9375977516174316);
		model.component("comp1").view("view1").axis().set("xmax", 9.56240177154541);
		model.component("comp1").view("view1").axis().set("ymin", -3.9234485626220703);
		model.component("comp1").view("view1").axis().set("ymax", 7.236551284790039);
		model.component("comp1").view("view1").axis().set("abstractviewlratio", -0.48418259620666504);
		model.component("comp1").view("view1").axis().set("abstractviewrratio", 0.8062990307807922);
		model.component("comp1").view("view1").axis().set("abstractviewbratio", -1.6363635063171387);
		model.component("comp1").view("view1").axis().set("abstractviewtratio", 1);
		model.component("comp1").view("view1").axis().set("abstractviewxscale", 0.0034129691775888205);
		model.component("comp1").view("view1").axis().set("abstractviewyscale", 0.0034129691775888205);

		model.component("comp1").material("mat1").label("Air [gas]");
		model.component("comp1").material("mat1").set("family", "custom");
		model.component("comp1").material("mat1").set("specular", "custom");
		model.component("comp1").material("mat1")
		.set("customspecular", new double[]{0.9803921568627451, 0.9803921568627451, 0.9803921568627451});
		model.component("comp1").material("mat1").set("diffuse", "custom");
		model.component("comp1").material("mat1")
		.set("customdiffuse", new double[]{0.9019607843137255, 0.9019607843137255, 1});
		model.component("comp1").material("mat1").set("ambient", "custom");
		model.component("comp1").material("mat1")
		.set("customambient", new double[]{0.9019607843137255, 0.9019607843137255, 1});
		model.component("comp1").material("mat1").set("noise", true);
		model.component("comp1").material("mat1").set("noisescale", 0.08);
		model.component("comp1").material("mat1").set("noisefreq", 3);
		model.component("comp1").material("mat1").set("lighting", "simple");
		model.component("comp1").material("mat1").info("Composition")
		.body("78.09 N2, 20.95 O2, 0.93 Ar, 0.039 CO2, trace others (vol%)");
		model.component("comp1").material("mat1").propertyGroup("def").func("k").set("arg", "T");
		model.component("comp1").material("mat1").propertyGroup("def").func("k")
		.set("pieces", new String[][]{{"70.0", "1000.0", "-8.404165E-4+1.107418E-4*T^1-8.635537E-8*T^2+6.31411E-11*T^3-1.88168E-14*T^4"}});
		model.component("comp1").material("mat1").propertyGroup("def").func("C").set("arg", "T");
		model.component("comp1").material("mat1").propertyGroup("def").func("C")
		.set("pieces", new String[][]{{"100.0", "375.0", "1010.97+0.0439479*T^1-2.922398E-4*T^2+6.503467E-7*T^3"}, {"375.0", "1300.0", "1093.29-0.6355521*T^1+0.001633992*T^2-1.412935E-6*T^3+5.59492E-10*T^4-8.663072E-14*T^5"}, {"1300.0", "3000.0", "701.0807+0.8493867*T^1-5.846487E-4*T^2+2.302436E-7*T^3-4.846758E-11*T^4+4.23502E-15*T^5"}});
		model.component("comp1").material("mat1").propertyGroup("def").func("rho_gas_2").set("arg", "T");
		model.component("comp1").material("mat1").propertyGroup("def").func("rho_gas_2")
		.set("pieces", new String[][]{{"80.0", "3000.0", "352.716*T^-1"}});
		model.component("comp1").material("mat1").propertyGroup("def").func("TD").set("arg", "T");
		model.component("comp1").material("mat1").propertyGroup("def").func("TD")
		.set("pieces", new String[][]{{"300.0", "753.0", "1.713214E-4-1.204913E-6*T^1+2.839046E-9*T^2-1.532799E-12*T^3"}, {"753.0", "873.0", "0.00416418-1.191227E-5*T^1+8.863636E-9*T^2"}});
		model.component("comp1").material("mat1").propertyGroup("def").func("eta").set("arg", "T");
		model.component("comp1").material("mat1").propertyGroup("def").func("eta")
		.set("pieces", new String[][]{{"120.0", "600.0", "-1.132275E-7+7.94333E-8*T^1-7.197989E-11*T^2+5.158693E-14*T^3-1.592472E-17*T^4"}, {"600.0", "2150.0", "3.892629E-6+5.75387E-8*T^1-2.675811E-11*T^2+9.709691E-15*T^3-1.355541E-18*T^4"}});
		model.component("comp1").material("mat1").propertyGroup("def")
		.set("thermalconductivity", new String[]{"k(T[1/K])[W/(m*K)]", "0", "0", "0", "k(T[1/K])[W/(m*K)]", "0", "0", "0", "k(T[1/K])[W/(m*K)]"});
		model.component("comp1").material("mat1").propertyGroup("def").set("heatcapacity", "C(T[1/K])[J/(kg*K)]");
		model.component("comp1").material("mat1").propertyGroup("def").set("density", "rho_gas_2(T[1/K])[kg/m^3]");
		model.component("comp1").material("mat1").propertyGroup("def").set("TD", "TD(T[1/K])[m^2/s]");
		model.component("comp1").material("mat1").propertyGroup("def").set("dynamicviscosity", "eta(T[1/K])[Pa*s]");
		model.component("comp1").material("mat1").propertyGroup("def")
		.set("relpermittivity", new String[]{"1", "0", "0", "0", "1", "0", "0", "0", "1"});
		model.component("comp1").material("mat1").propertyGroup("def").addInput("temperature");

		model.component("comp1").physics("es").feature("sfcd1").set("rhoqs", "1e-10");

		model.study().create("std1");
		model.study("std1").create("stat", "Stationary");

		model.sol().create("sol1");
		model.sol("sol1").study("std1");
		model.sol("sol1").attach("std1");
		model.sol("sol1").create("st1", "StudyStep");
		model.sol("sol1").create("v1", "Variables");
		model.sol("sol1").create("s1", "Stationary");
		model.sol("sol1").feature("s1").create("fc1", "FullyCoupled");
		model.sol("sol1").feature("s1").feature().remove("fcDef");

		model.result().numerical().create("max1", "MaxLine");
		model.result().numerical("max1").selection().set(new int[]{3});
		model.result().numerical("max1").set("probetag", "none");
		model.result().create("pg1", "PlotGroup2D");
		model.result("pg1").create("surf1", "Surface");
		model.result().export().create("tbl1", "Table");


		model.sol("sol1").attach("std1");
		model.sol("sol1").runAll();

		model.result().numerical("max1").set("table", "tbl1");
		model.result().numerical("max1").set("expr", new String[]{"V"});
		model.result().numerical("max1").set("unit", new String[]{"V"});
		model.result().numerical("max1").set("descr", new String[]{"Electric potential"});
		model.result().numerical("max1").setResult();
		model.result("pg1").label("Electric Potential (es)");
		model.result("pg1").set("frametype", "spatial");
		model.result("pg1").feature("surf1").set("resolution", "normal");
		model.result().export("tbl1").set("filename", "./tests/max.txt");
		model.result().export("tbl1").run();	
		return model;
	}

	public static void main(String[] args) throws IOException{
		run();
	}

}