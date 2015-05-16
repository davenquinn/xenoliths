from geotherm.models.geometry import stack_sections
from .forearc import forearc_section

# temperature of the base of the lithosphere
T_lithosphere = u(1300,"degC")

def instant_subduction(underplated_section, **kwargs):
    # Find the base of the lithosphere
    d = underplated_section.depth(T_lithosphere)
    distance = 100e3
    echo("Depth of the base of the "
        "lithosphere at the time of "
        "subduction:{0:.2f}".format(d))
    forearc = forearc_section(
            distance = distance,
            Tm = T_lithosphere.into("degC"),
            l = d.into("m"))
    echo("Temperature at subduction interface "
         "at the time of underplating: {0}"\
          .format(forearc.profile[-1]))

    return stack_sections(
        forearc,
        underplated_section)

