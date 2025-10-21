from django.db import models


class UserData(models.Model):
    def_id = models.AutoField(db_column="DEF_id", primary_key=True)
    def_timestamp = models.DateTimeField(
        db_column="DEF_timestamp", auto_now_add=True
    )
    username = models.CharField(unique=True, max_length=24, blank=True)
    firstname = models.CharField(max_length=24, blank=True, null=True)
    lastname = models.CharField(max_length=24, blank=True, null=True)
    password = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    ref_groupdata_group = models.IntegerField(
        default=3, db_column="REF|GroupData|group", blank=False, null=False
    )
    noleginon = models.IntegerField(blank=True, null=True)
    advanced = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.username

    class Meta:
        managed = False
        db_table = "UserData"
        ordering = ("username",)
        verbose_name_plural = "UserData"
        verbose_name = "UserData"


class SessionData(models.Model):
    def_id = models.AutoField(db_column="DEF_id", primary_key=True)
    def_timestamp = models.DateTimeField(
        db_column="DEF_timestamp", auto_now_add=True
    )
    name = models.TextField(blank=True, null=True)
    ref_userdata_user = models.ForeignKey(
        UserData,
        db_column="REF|UserData|user",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )
    image_path = models.TextField(db_column="image path", blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    hidden = models.IntegerField(blank=True, null=True)
    # ref_instrumentdata_instrument = models.IntegerField(
    #     db_column="REF|InstrumentData|instrument", blank=True, null=True
    # )
    ref_gridholderdata_holder = models.IntegerField(
        db_column="REF|GridHolderData|holder", blank=True, null=True
    )
    # frame_path = models.TextField(db_column="frame path", blank=True, null=True)

    def __str__(self) -> str:
        return self.name or "<no name>"

    class Meta:
        managed = False
        db_table = "SessionData"
        verbose_name = "SessionData"
        verbose_name_plural = "SessionData"


class CameraEMData(models.Model):
    def_id = models.AutoField(db_column="DEF_id", primary_key=True)
    def_timestamp = models.DateTimeField(
        db_column="DEF_timestamp", auto_now_add=True
    )
    ref_sessiondata_session = models.ForeignKey(
        SessionData,
        db_column="REF|SessionData|session",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )
    system_time = models.FloatField(
        db_column="system time", blank=True, null=True
    )
    subd_dimension_x = models.IntegerField(
        db_column="SUBD|dimension|x", blank=True, null=True
    )
    subd_dimension_y = models.IntegerField(
        db_column="SUBD|dimension|y", blank=True, null=True
    )
    subd_binning_x = models.IntegerField(
        db_column="SUBD|binning|x", blank=True, null=True
    )
    subd_binning_y = models.IntegerField(
        db_column="SUBD|binning|y", blank=True, null=True
    )
    binned_multiplier = models.FloatField(
        db_column="binned multiplier", blank=True, null=True
    )
    subd_offset_x = models.IntegerField(
        db_column="SUBD|offset|x", blank=True, null=True
    )
    subd_offset_y = models.IntegerField(
        db_column="SUBD|offset|y", blank=True, null=True
    )
    exposure_time = models.FloatField(
        db_column="exposure time", blank=True, null=True
    )
    exposure_type = models.TextField(
        db_column="exposure type", blank=True, null=True
    )
    exposure_timestamp = models.FloatField(
        db_column="exposure timestamp", blank=True, null=True
    )
    inserted = models.IntegerField(blank=True, null=True)
    dump = models.IntegerField(blank=True, null=True)
    subd_pixel_size_x = models.FloatField(
        db_column="SUBD|pixel size|x", blank=True, null=True
    )
    subd_pixel_size_y = models.FloatField(
        db_column="SUBD|pixel size|y", blank=True, null=True
    )
    energy_filtered = models.IntegerField(
        db_column="energy filtered", blank=True, null=True
    )
    energy_filter = models.IntegerField(
        db_column="energy filter", blank=True, null=True
    )
    energy_filter_width = models.FloatField(
        db_column="energy filter width", blank=True, null=True
    )
    nframes = models.IntegerField(blank=True, null=True)
    save_frames = models.IntegerField(
        db_column="save frames", blank=True, null=True
    )
    align_frames = models.IntegerField(
        db_column="align frames", blank=True, null=True
    )
    align_filter = models.TextField(
        db_column="align filter", blank=True, null=True
    )
    frames_name = models.TextField(
        db_column="frames name", blank=True, null=True
    )
    frame_time = models.FloatField(
        db_column="frame time", blank=True, null=True
    )
    frame_flip = models.IntegerField(
        db_column="frame flip", blank=True, null=True
    )
    frame_rotate = models.IntegerField(
        db_column="frame rotate", blank=True, null=True
    )
    temperature = models.FloatField(blank=True, null=True)
    temperature_status = models.TextField(
        db_column="temperature status", blank=True, null=True
    )
    readout_delay = models.IntegerField(
        db_column="readout delay", blank=True, null=True
    )
    gain_index = models.IntegerField(
        db_column="gain index", blank=True, null=True
    )
    system_corrected = models.IntegerField(
        db_column="system corrected", blank=True, null=True
    )
    ref_instrumentdata_ccdcamera = models.IntegerField(
        db_column="REF|InstrumentData|ccdcamera", blank=True, null=True
    )
    seq_use_frames = models.TextField(
        db_column="SEQ|use frames", blank=True, null=True
    )

    def __str__(self) -> str:
        session = "<no session>"
        if s := self.ref_sessiondata_session:
            session = s.name
        return "%s|%s" % (session, self.def_timestamp)

    class Meta:
        managed = False
        verbose_name = "CameraEMData"
        verbose_name_plural = "CameraEMData"
        db_table = "CameraEMData"


class AcquisitionImageData(models.Model):
    def_id = models.AutoField(db_column="DEF_id", primary_key=True)
    def_timestamp = models.DateTimeField(
        db_column="DEF_timestamp", auto_now_add=True
    )
    ref_sessiondata_session = models.ForeignKey(
        SessionData,
        db_column="REF|SessionData|session",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )
    mrc_image = models.TextField(db_column="MRC|image", blank=True, null=True)
    pixeltype = models.TextField(blank=True, null=True)
    pixels = models.IntegerField(blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    filename = models.TextField(blank=True, null=True)
    ref_imagelistdata_list = models.IntegerField(
        db_column="REF|ImageListData|list", blank=True, null=True
    )
    ref_queuedata_queue = models.IntegerField(
        db_column="REF|QueueData|queue", blank=True, null=True
    )
    ref_scopeemdata_scope = models.IntegerField(
        db_column="REF|ScopeEMData|scope", blank=True, null=True
    )
    ref_cameraemdata_camera = models.ForeignKey(
        CameraEMData,
        db_column="REF|CameraEMData|camera",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )
    ref_correctorplandata_corrector_plan = models.IntegerField(
        db_column="REF|CorrectorPlanData|corrector plan", blank=True, null=True
    )
    correction_channel = models.IntegerField(
        db_column="correction channel", blank=True, null=True
    )
    channel = models.IntegerField(blank=True, null=True)
    ref_darkimagedata_dark = models.IntegerField(
        db_column="REF|DarkImageData|dark", blank=True, null=True
    )
    ref_brightimagedata_bright = models.IntegerField(
        db_column="REF|BrightImageData|bright", blank=True, null=True
    )
    ref_normimagedata_norm = models.IntegerField(
        db_column="REF|NormImageData|norm", blank=True, null=True
    )
    ref_presetdata_preset = models.IntegerField(
        db_column="REF|PresetData|preset", blank=True, null=True
    )
    ref_acquisitionimagetargetdata_target = models.IntegerField(
        db_column="REF|AcquisitionImageTargetData|target", blank=True, null=True
    )
    ref_emtargetdata_emtarget = models.IntegerField(
        db_column="REF|EMTargetData|emtarget", blank=True, null=True
    )
    ref_griddata_grid = models.IntegerField(
        db_column="REF|GridData|grid", blank=True, null=True
    )
    ref_spotwellmapdata_spotmap = models.IntegerField(
        db_column="REF|SpotWellMapData|spotmap", blank=True, null=True
    )
    ref_tiltseriesdata_tilt_series = models.IntegerField(
        db_column="REF|TiltSeriesData|tilt series", blank=True, null=True
    )
    version = models.IntegerField(blank=True, null=True)
    tiltnumber = models.IntegerField(blank=True, null=True)
    ref_moverparamsdata_mover = models.IntegerField(
        db_column="REF|MoverParamsData|mover", blank=True, null=True
    )
    seq_use_frames = models.TextField(
        db_column="SEQ|use frames", blank=True, null=True
    )

    def __str__(self) -> str:
        return self.mrc_image or "<no mrc>"

    class Meta:
        managed = False
        verbose_name = "AcquisitionImageData"
        verbose_name_plural = "AcquisitionImageData"
        db_table = "AcquisitionImageData"
