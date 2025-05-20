set DESIGN_NAME $design_name
set DESIGN_NAME_i $design_name_i
set FILE_FORMAT $file_format
set FILE_FORMAT_REF $file_format_ref

set RTL_DIR "XXX"

#------------------------------------------------------------------------------
# Setup the libraries
#------------------------------------------------------------------------------
    set search_path [list ./rtl]
    set all_dbs [list /XXX/lib/NangateOpenCellLibrary_PDKv1_3_v2010_12/db/typical.db]

#------------------------------------------------------------------------------
# Read reference design
#------------------------------------------------------------------------------
    if {${FILE_FORMAT_REF} == "verilog"} {
        read_verilog -container r ${RTL_DIR}/${DESIGN_NAME}_ref/${DESIGN_NAME}_ref.v
    } elseif {${FILE_FORMAT_REF} == "sverilog"} {
        read_sverilog -container r ${RTL_DIR}/${DESIGN_NAME}_ref/${DESIGN_NAME}_ref.sv
    } else {
        read_vhdl -container r ${RTL_DIR}/${DESIGN_NAME}_ref/${DESIGN_NAME}_ref.v
    }
    set_top ${DESIGN_NAME}_ref

#------------------------------------------------------------------------------
# Read implementation design
#------------------------------------------------------------------------------
    if {${FILE_FORMAT} == "verilog"} {
        read_verilog -container i ${RTL_DIR}/${DESIGN_NAME_i}/${DESIGN_NAME_i}.v
    } elseif {${FILE_FORMAT} == "sverilog"} {
        read_sverilog -container i ${RTL_DIR}/${DESIGN_NAME_i}/${DESIGN_NAME_i}.sv
    } else {
        read_vhdl -container i ${RTL_DIR}/${DESIGN_NAME_i}/${DESIGN_NAME_i}.v
    }
    set_top ${DESIGN_NAME_i}

#------------------------------------------------------------------------------
# Perform formal verification
#------------------------------------------------------------------------------
    match

    verify

#------------------------------------------------------------------------------
# Generate reports
#------------------------------------------------------------------------------
    report_unmatched_points > unmatched_points.rpt
    report_passing_points > passing_points.rpt
    report_failing_points -list -matched > failing_points.rpt
    analyze_points -all > points.rpt

    exit