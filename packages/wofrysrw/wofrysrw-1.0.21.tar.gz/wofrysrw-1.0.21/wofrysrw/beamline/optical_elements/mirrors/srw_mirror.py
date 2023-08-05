import numpy

from syned.beamline.optical_elements.mirrors.mirror import Mirror
from syned.beamline.shape import Rectangle, Ellipse, Circle

from wofrysrw.beamline.optical_elements.srw_optical_element import SRWOpticalElement, Orientation
from wofrysrw.propagator.wavefront2D.srw_wavefront import WavefrontPropagationParameters

from srwlib import SRWLOptC, SRWLOptMir
from srwlib import srwl, srwl_opt_setup_surf_height_1d, srwl_opt_setup_surf_height_2d, srwl_uti_read_data_cols


class ApertureShape:
    RECTANGULAR = 'r'
    ELLIPTIC = 'e'

class SimulationMethod:
    THIN = 1
    THICK = 2

class TreatInputOutput:
    WAVEFRONT_INPUT_PLANE_BEFORE_OUTPUT_PLANE_AFTER  = 0
    WAVEFRONT_INPUT_CENTER_OUTPUT_CENTER  = 1
    WAVEFRONT_INPUT_CENTER_OUTPUT_CENTER_DRIFT_BACK  = 2

class ScaleType:
    LINEAR = 'lin'
    LOGARITHMIC = 'log'

class SRWMirror(Mirror, SRWOpticalElement):
    def __init__(self,
                 name                               = "Undefined",
                 tangential_size                    = 1.2,
                 sagittal_size                      = 0.01,
                 vertical_position_of_mirror_center = 0.0,
                 horizontal_position_of_mirror_center = 0.0,
                 grazing_angle                      = 0.003,
                 orientation_of_reflection_plane    = Orientation.UP,
                 invert_tangent_component           = False,
                 height_profile_data_file           = "mirror.dat",
                 height_profile_data_file_dimension = 1,
                 height_amplification_coefficient   = 1.0):


        Mirror.__init__(self,
                        name=name,
                        boundary_shape=Rectangle(x_left=horizontal_position_of_mirror_center - 0.5*sagittal_size,
                                                 x_right=horizontal_position_of_mirror_center + 0.5*sagittal_size,
                                                 y_bottom=vertical_position_of_mirror_center - 0.5*tangential_size,
                                                 y_top=vertical_position_of_mirror_center + 0.5*tangential_size),
                        surface_shape=self.get_shape())

        self.tangential_size                                  = tangential_size
        self.sagittal_size                                    = sagittal_size
        self.grazing_angle                                    = grazing_angle
        self.orientation_of_reflection_plane                  = orientation_of_reflection_plane
        self.invert_tangent_component                         = invert_tangent_component

        self.height_profile_data_file = height_profile_data_file
        self.height_profile_data_file_dimension = height_profile_data_file_dimension
        self.height_amplification_coefficient = height_amplification_coefficient

    def get_shape(self):
        raise NotImplementedError()

    def applyOpticalElement(self, wavefront=None, parameters=None):
        optical_elements = [self.toSRWLOpt()]
        propagation_parameters = [self.get_srw_wavefront_propagation_parameter(parameters)]

        if not self.height_profile_data_file is None:
            optical_elements.append(self.get_optTrEr())
            propagation_parameters.append(WavefrontPropagationParameters().to_SRW_array())

        optBL = SRWLOptC(optical_elements, propagation_parameters)

        srwl.PropagElecField(wavefront, optBL)

        return wavefront

    def add_to_srw_native_array(self, oe_array = [], pp_array=[], parameters=None, wavefront=None):
        super(SRWMirror, self).add_to_srw_native_array(oe_array, pp_array, parameters)

        if not self.height_profile_data_file is None:
            oe_array.append(self.get_optTrEr())
            pp_array.append(WavefrontPropagationParameters().to_SRW_array())

    def get_optTrEr(self):
        if self.orientation_of_reflection_plane == Orientation.LEFT or self.orientation_of_reflection_plane == Orientation.RIGHT:
            dim = 'x'
        elif self.orientation_of_reflection_plane == Orientation.UP or self.orientation_of_reflection_plane == Orientation.DOWN:
            dim = 'y'

        if self.height_profile_data_file_dimension == 1:
            height_profile_data = srwl_uti_read_data_cols(self.height_profile_data_file,
                                                          _str_sep='\t',
                                                          _i_col_start=0,
                                                          _i_col_end=1)

            optTrEr = srwl_opt_setup_surf_height_1d(_height_prof_data=height_profile_data,
                                                    _ang=self.grazing_angle,
                                                    _dim=dim,
                                                    _amp_coef=self.height_amplification_coefficient)
        elif self.height_profile_data_file_dimension == 2:
            height_profile_data = srwl_uti_read_data_cols(self.height_profile_data_file,
                                                          _str_sep='\t')

            optTrEr = srwl_opt_setup_surf_height_2d(_height_prof_data=height_profile_data,
                                                    _ang=self.grazing_angle,
                                                    _dim=dim,
                                                    _amp_coef=self.height_amplification_coefficient)
        return optTrEr

    def toSRWLOpt(self):
        nvx, nvy, nvz, tvx, tvy = self.get_orientation_vectors()
        x, y = self.getXY()

        if isinstance(self.get_boundary_shape(), Rectangle):
            ap_shape = ApertureShape.RECTANGULAR
        elif isinstance(self.get_boundary_shape(), Ellipse) or isinstance(self.get_boundary_shape(), Circle):
            ap_shape = ApertureShape.ELLIPTIC

        return self.get_SRWLOptMir(nvx, nvy, nvz, tvx, tvy, x, y, ap_shape)

    def get_SRWLOptMir(self, nvx, nvy, nvz, tvx, tvy, x, y, ap_shape):
        mirror = SRWLOptMir()

        mirror.set_dim_sim_meth(_size_tang=self.tangential_size,
                                _size_sag=self.sagittal_size,
                                _ap_shape=ap_shape,
                                _sim_meth=SimulationMethod.THICK,
                                _treat_in_out=TreatInputOutput.WAVEFRONT_INPUT_CENTER_OUTPUT_CENTER)
        mirror.set_orient(_nvx=nvx,
                          _nvy=nvy,
                          _nvz=nvz,
                          _tvx=tvx,
                          _tvy=tvy,
                          _x = x,
                          _y = y)

        return mirror

    def fromSRWLOpt(self, srwlopt=SRWLOptMir()):
        if not isinstance(srwlopt, SRWLOptMir):
            raise ValueError("SRW object is not a SRWLOptMir object")

        if srwlopt.tvx != 0.0:
            orientation_of_reflection_plane = Orientation.LEFT if srwlopt.nvx < 0 else Orientation.RIGHT
            grazing_angle = abs(numpy.arctan(srwlopt.nvz/srwlopt.nvx))
            if orientation_of_reflection_plane == Orientation.LEFT: invert_tangent_component = numpy.sign(srwlopt.nvz) == numpy.sign(srwlopt.tvx)
            else: invert_tangent_component = numpy.sign(srwlopt.nvz) != numpy.sign(srwlopt.tvx)
        elif srwlopt.tvy != 0.0:
            orientation_of_reflection_plane = Orientation.DOWN if srwlopt.nvy < 0 else Orientation.UP
            grazing_angle = abs(numpy.arctan(srwlopt.nvz/srwlopt.nvy))
            if orientation_of_reflection_plane == Orientation.UP: invert_tangent_component = numpy.sign(srwlopt.nvy) == numpy.sign(srwlopt.tvy)
            else: invert_tangent_component = numpy.sign(srwlopt.nvy) != numpy.sign(srwlopt.tvy)
        else:
            raise ValueError("Tangential orientation angles (tvx/tvy) are both 0.0!")

        self.__init__(tangential_size                 = srwlopt.dt,
                      sagittal_size                   = srwlopt.ds,
                      grazing_angle                   = grazing_angle,
                      orientation_of_reflection_plane = orientation_of_reflection_plane,
                      invert_tangent_component        = invert_tangent_component,
                      height_profile_data_file        = None)

    def to_python_code(self, data=None):
        oe_name = data[0]

        nvx, nvy, nvz, tvx, tvy = self.get_orientation_vectors()
        x, y = self.getXY()

        if isinstance(self.get_boundary_shape(), Rectangle):
            ap_shape = ApertureShape.RECTANGULAR
        elif isinstance(self.get_boundary_shape(), Ellipse) or isinstance(self.get_boundary_shape(), Circle):
            ap_shape = ApertureShape.ELLIPTIC

        text_code = oe_name + " = " + self.to_python_code_aux(nvx, nvy, nvz, tvx, tvy, x, y, ap_shape)

        text_code += oe_name + ".set_dim_sim_meth(_size_tang=" + str(self.tangential_size) + "," + "\n"
        text_code += "                      _size_sag=" + str(self.sagittal_size) + "," + "\n"
        text_code += "                      _ap_shape='" + str(ap_shape) + "'," + "\n"
        text_code += "                      _sim_meth=" + str(SimulationMethod.THICK) + "," + "\n"
        text_code += "                      _treat_in_out=" + str(TreatInputOutput.WAVEFRONT_INPUT_CENTER_OUTPUT_CENTER) + ")" + "\n"

        text_code += oe_name + ".set_orient(_nvx=" + str(nvx) + "," + "\n"
        text_code += "                 _nvy=" + str(nvy) + "," + "\n"
        text_code += "                 _nvz=" + str(nvz) + "," + "\n"
        text_code += "                 _tvx=" + str(tvx) + "," + "\n"
        text_code += "                 _tvy=" + str(tvy) + "," + "\n"
        text_code += "                 _x=" + str(x) + "," + "\n"
        text_code += "                 _y=" + str(y) + ")" + "\n"

        text_code += "\n"

        if not self.height_profile_data_file is None:
            text_code += "\n"

            if self.orientation_of_reflection_plane == Orientation.LEFT or self.orientation_of_reflection_plane == Orientation.RIGHT:
                dim = 'x'
            elif self.orientation_of_reflection_plane == Orientation.UP or self.orientation_of_reflection_plane == Orientation.DOWN:
                dim = 'y'

            if self.height_profile_data_file_dimension == 1:
                text_code += "height_profile_data = srwl_uti_read_data_cols('" + self.height_profile_data_file + "'," + "\n"
                text_code += "                                              _str_sep='\\t'," + "\n"
                text_code += "                                              _i_col_start=0," + "\n"
                text_code += "                                              _i_col_end=1)" + "\n"

                text_code += "optTrEr_" + oe_name + " = srwl_opt_setup_surf_height_1d(_height_prof_data=height_profile_data," + "\n"
                text_code += "                                                        _ang="+ str(self.grazing_angle) + "," + "\n"
                text_code += "                                                        _dim='"+ dim + "'," + "\n"
                text_code += "                                                        _amp_coef="+ str(self.height_amplification_coefficient) + ")" + "\n"

            elif self.height_profile_data_file_dimension == 2:
                text_code += "height_profile_data = srwl_uti_read_data_cols('" + self.height_profile_data_file + "'," + "\n"
                text_code += "                                              _str_sep='\\t')" + "\n"

                text_code += "optTrEr_" + oe_name + " = srwl_opt_setup_surf_height_2d(_height_prof_data=height_profile_data," + "\n"
                text_code += "                                                        _ang="+ str(self.grazing_angle) + "," + "\n"
                text_code += "                                                        _dim='"+ dim + "'," + "\n"
                text_code += "                                                        _amp_coef="+ str(self.height_amplification_coefficient) + ")" + "\n"

        return text_code
