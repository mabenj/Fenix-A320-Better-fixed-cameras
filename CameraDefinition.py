import copy


class CameraDefinition:
    VIRTUAL_COCKPIT = [-0.5, 1.2, 13.39]

    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.zoom = kwargs["zoom"]
        self.pbh = kwargs["pbh"]
        self.xyz = kwargs["xyz"]
        self.is_cabin = kwargs.get("is_cabin", False)
        center_origin = kwargs.get("center_origin", False)
        if center_origin == False:
            self.xyz[0] += CameraDefinition.VIRTUAL_COCKPIT[0]
            self.xyz[1] += CameraDefinition.VIRTUAL_COCKPIT[1]
            self.xyz[2] += CameraDefinition.VIRTUAL_COCKPIT[2]

    def get_mirrored(self):
        copied = copy.deepcopy(self)
        copied.xyz[0] = -copied.xyz[0]
        copied.pbh[2] = -copied.pbh[2]
        return copied