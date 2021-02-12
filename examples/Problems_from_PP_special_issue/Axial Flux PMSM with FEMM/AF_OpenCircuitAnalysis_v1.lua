-- Analysis parameters
radius = 300 -- mm
iterations = 1
displacement_inc = 10/50 -- mm
mydir = "./"
open(mydir .. "AF_AntiPeriodic.fem")

file_out = openfile(mydir .. "output.txt" , "w")

for i = 0, iterations do
    mi_analyze()
    mi_loadsolution()
    mo_groupselectblock(2)
    fx = mo_blockintegral(18)
    torque = fx*radius/1000*14
    displ = i*displacement_inc
    write(file_out, i, ",", displ, "," , torque, ",", radius, ",", a, ",", b, "\n")
    if (i < iterations) then
        mi_selectgroup(2)
        mi_movetranslate(displacement_inc, 0)
    end
end

closefile(file_out)

mo_close()
mi_close()
quit()