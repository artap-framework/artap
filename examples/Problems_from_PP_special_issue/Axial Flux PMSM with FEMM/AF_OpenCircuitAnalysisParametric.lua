------------
-- Variables -- the code gets these parameters from artap
--pp = 0.8 -- relative pole pitch: 0.4 - 0.99
--p_offset = 0.8 -- relative offset: 0 - 0.99
------------
-- Analysis parameters
iterations=2
radius=300 -- mm
displacement_inc=10/iterations -- mm
length = 134.64
l_mag = length / 2 * pp
offset = length / 2 * (1 - pp) * p_offset
x0 = 11.22
h_mag = 10
------------

showconsole()
clearconsole()
mydir="./"
open(mydir .. "AF_PeriodicParametric.fem")
mi_saveas(mydir .. "temp.fem")

xm1 = x0 + l_mag / 2
xm2 = x0 + length / 2 - l_mag / 2 + offset
xm3 = x0 + length / 2 + l_mag / 2 + offset
xm4 = x0 + length - l_mag / 2
ymu = 0 + h_mag
ymd = 0

mi_addnode(xm1,ymd)
mi_addnode(xm2,ymd)
mi_addnode(xm3,ymd)
mi_addnode(xm4,ymd)
mi_addnode(xm1,ymu)
mi_addnode(xm2,ymu)
mi_addnode(xm3,ymu)
mi_addnode(xm4,ymu)

mi_addsegment(x0,ymd,xm1,ymd)
mi_addsegment(x0,ymu,xm1,ymu)
mi_addsegment(xm1,ymd,xm2,ymd)
mi_addsegment(xm1,ymu,xm2,ymu)
mi_addsegment(xm2,ymd,xm3,ymd)
mi_addsegment(xm2,ymu,xm3,ymu)
mi_addsegment(xm3,ymd,xm4,ymd)
mi_addsegment(xm3,ymu,xm4,ymu)
mi_addsegment(xm4,ymd,x0+length,ymd)
mi_addsegment(xm4,ymu,x0+length,ymu)
mi_addsegment(xm1,ymd,xm1,ymu)
mi_addsegment(xm2,ymd,xm2,ymu)
mi_addsegment(xm3,ymd,xm3,ymu)
mi_addsegment(xm4,ymd,xm4,ymu)

mi_selectsegment((x0+xm1)/2,ymd)
mi_selectsegment((x0+xm1)/2,ymu)
mi_selectsegment((xm1+xm2)/2,ymd)
mi_selectsegment((xm1+xm2)/2,ymu)
mi_selectsegment((xm2+xm3)/2,ymd)
mi_selectsegment((xm2+xm3)/2,ymu)
mi_selectsegment((xm3+xm4)/2,ymd)
mi_selectsegment((xm3+xm4)/2,ymu)
mi_selectsegment((xm4+x0+length)/2,ymd)
mi_selectsegment((xm4+x0+length)/2,ymu)
mi_selectsegment(xm1,(ymd+ymu)/2)
mi_selectsegment(xm2,(ymd+ymu)/2)
mi_selectsegment(xm3,(ymd+ymu)/2)
mi_selectsegment(xm4,(ymd+ymu)/2)
mi_setgroup(2)
mi_clearselected()

mi_addblocklabel((x0+xm1)/2,(ymd+ymu)/2)
mi_selectlabel((x0+xm1)/2,(ymd+ymu)/2)
mi_setblockprop('N38',1,0,'None',-90,2,0)
mi_clearselected()

mi_addblocklabel((xm2+xm3)/2,(ymd+ymu)/2)
mi_selectlabel((xm2+xm3)/2,(ymd+ymu)/2)
mi_setblockprop('N38',1,0,'None',90,2,0)
mi_clearselected()

mi_addblocklabel((xm4+x0+length)/2,(ymd+ymu)/2)
mi_selectlabel((xm4+x0+length)/2,(ymd+ymu)/2)
mi_setblockprop('N38',1,0,'None',-90,2,0)
mi_clearselected()

mi_addblocklabel((xm1+xm2)/2,(ymd+ymu)/2)
mi_selectlabel((xm1+xm2)/2,(ymd+ymu)/2)
mi_setblockprop('Air',1,0,'None',0,2,0)
mi_clearselected()

mi_addblocklabel((xm3+xm4)/2,(ymd+ymu)/2)
mi_selectlabel((xm3+xm4)/2,(ymd+ymu)/2)
mi_setblockprop('Air',1,0,'None',0,2,0)
mi_clearselected()

mi_seteditmode("group")

outfile = openfile("output.txt", "w")

for i=0,iterations do
    mi_analyze()
    mi_loadsolution()
    mo_groupselectblock(2)
    fx=mo_blockintegral(18)
    torque=fx*radius/1000*14
    displ=i*displacement_inc
    write(outfile, torque, ",")
    if (i<iterations) then
        mi_selectgroup(2)
        mi_movetranslate(displacement_inc,0)
    end
end

mo_close()
mi_close()

closefile(outfile)
quit()