 from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3

class StaticRouting(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(StaticRouting, self).__init__(*args, **kwargs)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst
        )
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        dpid = datapath.id

        # 🔹 s1
        if dpid == 1:
            # h1 → s3
            self.add_flow(datapath, 100,
                          parser.OFPMatch(in_port=1),
                          [parser.OFPActionOutput(3)])

            # s3 → h1
            self.add_flow(datapath, 100,
                          parser.OFPMatch(in_port=3),
                          [parser.OFPActionOutput(1)])

        # 🔹 s2 (blocked)
        elif dpid == 2:
            pass

        # 🔹 s3
        elif dpid == 3:
            # s1 → h3
            self.add_flow(datapath, 100,
                          parser.OFPMatch(in_port=1),
                          [parser.OFPActionOutput(2)])

            # h3 → s1
            self.add_flow(datapath, 100,
                          parser.OFPMatch(in_port=2),
                          [parser.OFPActionOutput(1)])

    # 🔥 PACKET_IN HANDLER (ADDED)
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        in_port = msg.match['in_port']
        dpid = datapath.id

        actions = []

        # s1 forwarding
        if dpid == 1:
            if in_port == 1:
                actions = [parser.OFPActionOutput(3)]
            elif in_port == 3:
                actions = [parser.OFPActionOutput(1)]

        # s3 forwarding
        elif dpid == 3:
            if in_port == 1:
                actions = [parser.OFPActionOutput(2)]
            elif in_port == 2:
                actions = [parser.OFPActionOutput(1)]

        # s2 blocked (no actions)

        # Send packet if allowed
        if actions:
            out = parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=ofproto.OFP_NO_BUFFER,
                in_port=in_port,
                actions=actions,
                data=msg.data
            )
            datapath.send_msg(out)
