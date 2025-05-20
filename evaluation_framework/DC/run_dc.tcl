set DESIGN_NAME $design_name
set CLOCK_PORT  $clock_name
set FILE_FORMAT $file_format
set FINAL_VERILOG_OUTPUT_FILE "${design_name}.mapped.v"
set FINAL_SDC_OUTPUT_FILE     "${design_name}.mapped.sdc"

set REPORTS_DIR "report"
set RESULTS_DIR "results"

file mkdir ${REPORTS_DIR}
file mkdir ${RESULTS_DIR}

#------------------------------------------------------------------------------
# Setup the libraries
#------------------------------------------------------------------------------
    set_app_var target_library $all_dbs
    set_app_var link_library $all_links

    saif_map -start
    set_app_var compile_enable_register_merging false
    set_app_var compile_clock_gating_through_hierarchy false
    set_app_var compile_sequential_area_recovery false

#------------------------------------------------------------------------------
# Read design
#------------------------------------------------------------------------------
    define_design_lib WORK -path ./WORK

    if {${FILE_FORMAT} == "verilog"} {
    analyze -format verilog -recursive -autoread $rtl_path -top ${DESIGN_NAME}
    } elseif {${FILE_FORMAT} == "sverilog"} {
        analyze -format sverilog -recursive -autoread $rtl_path -top ${DESIGN_NAME}
    } else {
        analyze -format vhdl -recursive -autoread $rtl_path -top ${DESIGN_NAME}
    }
    elaborate ${DESIGN_NAME}

#------------------------------------------------------------------------------
# Setup the clock
#------------------------------------------------------------------------------

    set CLOCK_PERIOD 0.1  

    if {[sizeof_collection [get_ports clk]] > 0} {
        create_clock -name clk -period $CLOCK_PERIOD [get_ports clk]
        set CLOCK_REF clk  ;
        set_max_delay -from [all_inputs] -to [all_registers] $CLOCK_PERIOD
        set_max_delay -from [all_registers] -to [all_outputs] $CLOCK_PERIOD
    } else {
        create_clock -name vclk -period $CLOCK_PERIOD 
        set CLOCK_REF vclk ; 
    }

    set_max_delay -from [all_inputs] -to [all_outputs] $CLOCK_PERIOD
    

    # set OUTPUT_DELAY [expr 0.3 * $CLOCK_PERIOD]
    # set_output_delay -clock $CLOCK_REF -max $OUTPUT_DELAY [all_outputs]

#------------------------------------------------------------------------------
# Check for design errors
#------------------------------------------------------------------------------
    # Prevent assignment statements in the Verilog netlist.
    set_fix_multiple_port_nets -all -buffer_constants -feedthroughs [all_designs]

    check_design -summary
    check_design > ${REPORTS_DIR}/check_design.rpt

#------------------------------------------------------------------------------
# Set DRC constraints 
#------------------------------------------------------------------------------

    set_auto_disable_drc_nets -constant false
    set_transform_for_retiming [get_cells *] dont_retime

#-----------------------------------------------------------------------------
# Compile the design
#-----------------------------------------------------------------------------
    set compile_cmd "compile"
    echo $compile_cmd
    eval $compile_cmd

    ungroup -all -flatten
    change_names -rules verilog -hierarchy

#--------------------------------------------------------------------------------
# Generate final reports
#--------------------------------------------------------------------------------

    report_qor > ${REPORTS_DIR}/qor.rpt
    report_timing -transition_time -nets -attributes -nosplit -max_paths 10 > ${REPORTS_DIR}/timing.rpt
    report_area -nosplit -hierarchy > ${REPORTS_DIR}/area.rpt
    report_power -nosplit > ${REPORTS_DIR}/power.rpt
    write -format verilog -hierarchy -output ${RESULTS_DIR}/${FINAL_VERILOG_OUTPUT_FILE}

    exit
    
