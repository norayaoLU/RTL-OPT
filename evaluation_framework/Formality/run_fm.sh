#!/bin/bash

design_name="ticket_machine"
design_name_i="ticket_machine_gpt"
file_format="verilog"
file_format_ref="verilog"

FM_DIR=`pwd`

DIR=${FM_DIR}/${design_name}_rpt
mkdir $DIR; cd $DIR

fm_shell -x "
    set design_name $design_name;
    set design_name_i $design_name_i;
    set file_format $file_format;
    set file_format_ref $file_format_ref;
    source -e -v ../run_fm.tcl;
"

cd ..