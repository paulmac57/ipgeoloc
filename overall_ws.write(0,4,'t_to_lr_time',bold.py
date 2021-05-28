overall_ws.write(0,4,'t_to_lr_time',bold_o)
    overall_ws.write(0,5,'t_to_lr_ixp_ip',bold_o)
    overall_ws.write(0,6,'t_to_lr_ixp_lat',bold_o)
    overall_ws.write(0,7,'t_to_lr_ixp_lon',bold_o)
    overall_ws.write(0,8,'t_to_lr_lr_ip',bold_o)


    overall_ws.write(0,9,'s_to_t_time',bold_o)
    overall_ws.write(0,10,'s_to_t_s_ip',bold_o)
    overall_ws.write(0,11,'s_to_t_s_id',bold_o)
    overall_ws.write(0,12,'s_to_t_s_lat',bold_o)
    overall_ws.write(0,13,'s_to_t_s_lon',bold_o)
    overall_ws.write(0,14,'s_to_t_ixp_ip',bold_o)
    overall_ws.write(0,15,'s_to_t_ixp_lat',bold_o)
    overall_ws.write(0,16,'s_to_t_ixp_lon',bold_o)
    overall_ws.write(0,17,'s_to_t_lr_ip',bold_o)

    overall_ws.write(0,18,'s_to_lr_time',bold_o)
    overall_ws.write(0,19,'s_to_lr_s_ip',bold_o)
    overall_ws.write(0,20,'s_to_lr_s_id',bold_o)
    overall_ws.write(0,21,'s_to_lr_s_lat',bold_o)
    overall_ws.write(0,22,'s_to_lr_s_lon',bold_o)
    overall_ws.write(0,23,'s_to_lr_ixp_ip',bold_o)
    overall_ws.write(0,24,'s_to_lr_ixp_lat',bold_o)
    overall_ws.write(0,25,'s_to_lr_ixp_lon',bold_o)
    overall_ws.write(0,26,'s_to_lr_lr_ip',bold_o)

    overall_ws.write(0,27,'i_to_lr_time',bold_o)
    overall_ws.write(0,28,'i_to_lr_ixp_ip',bold_o)
    overall_ws.write(0,29,'i_to_lr_ixp_lat',bold_o)
    overall_ws.write(0,30,'i_to_lr_ixp_lon',bold_o)
    overall_ws.write(0,31,'i_to_lr_lr_ip',bold_o)

    overall_ws.write(0,32,'i_to_t_time',bold_o)
    overall_ws.write(0,33,'i_to_t_ixp_ip',bold_o)
    overall_ws.write(0,34,'i_to_t_ixp_lat',bold_o)
    overall_ws.write(0,35,'i_to_t_ixp_lon',bold_o)
    overall_ws.write(0,36,'i_to_t_lr_ip',bold_o)

    measurement_dict[this_measurement]['target_probe']      = target_info[0]
        measurement_dict[this_measurement]['target_lat']        = target_info[1]
        measurement_dict[this_measurement]['target_lon']        = target_info[2]
        measurement_dict[this_measurement]['target_asn']        = target_info[3]
        measurement_dict[this_measurement]['target_ip']         = target_info[4]
        measurement_dict[this_measurement]['target_isanchor']   = target_info[5]