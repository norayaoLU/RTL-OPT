#!/bin/bash

RTL_DIR="XXX"
DC_DIR=`pwd`
TECH_DIR="XXX" ### in ./b14

LIST_DESIGN=`cat design_list`

FLAG=0
RUNTIME=0

for DESIGN in $LIST_DESIGN
do
	if [ $FLAG -eq 0 ]; then
		if [ "$DESIGN" == '__START__' ]; then 
			FLAG=1 
			continue
		else continue;
		fi
	fi

	if [ "$DESIGN" == '__END__' ]; then break; fi

	DIR=${DC_DIR}/${DESIGN}
	mkdir $DIR; cd $DIR
	echo "Starting"
	stamp_begin=`date +%s`;
	dc_shell -x "
		echo [date]; 
		set bench_root $RTL_DIR;
		set design     $DESIGN;
        	source ../set_rtl_path.tcl;
		source ../tech_nangate.tcl
		echo [date]; 
		source -e -v ../run_dc.tcl;
		" 
		#source $TECH_DIR/tech.tcl
	stamp_end=`date +%s`;
	((RUNTIME += stamp_end - stamp_begin));
done

echo ""
echo "Runtime: ${RUNTIME} seconds"
echo ""
cd ..
