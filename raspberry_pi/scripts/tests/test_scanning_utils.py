import numpy as np
from ..utils.scanning_utils import extract_ids, preprocess

class TestScanningUtils:
  def test_extract_ids_correct(self):
    x = "a peppi id 123456 and a student id 1234567"

    student_id, peppi_id = extract_ids(x)

    assert student_id == "1234567" and peppi_id == "123456"

  def test_extract_ids_one_wrong(self):
    x = "a wrong id 12345658741 and a right id 1234567 should get the second one"

    student_id, peppi_id = extract_ids(x)

    assert student_id == "1234567" and peppi_id == None

  def test_extract_ids_both_wrong(self):
    x = "a wrong id 123456842ff and a wrong id 1687469827 should get neither one"

    student_id, peppi_id = extract_ids(x)

    assert student_id == None and peppi_id == None

  def test_preprocess_smoke(self):
    #Generate a black image
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)

    #Preprocess it
    processed_image = preprocess(dummy_image)

    #Make sure it is the right shape
    assert processed_image.shape == (100, 100)