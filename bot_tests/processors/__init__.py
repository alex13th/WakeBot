from .t_default import DefaultProcessorTestCase
from .t_reserve import ReserveProcessorTestCase
from .t_wake import WakeProcessorTestCase
from .t_supboard import SupboardProcessorTestCase
from .t_bathhouse import BathhouseProcessorTestCase

if __name__ == "__main__":
    DefaultProcessorTestCase, ReserveProcessorTestCase
    WakeProcessorTestCase, SupboardProcessorTestCase
    BathhouseProcessorTestCase
