from ambiegen.generators.obstacle_generator import ObstacleGenerator
from testcase import TestCase
from aerialist.px4.obstacle import Obstacle
def test_genotype2phenotype():
    # Create an instance of ObstacleGenerator
    
    min_size = Obstacle.Size(2, 2, 15)
    max_size = Obstacle.Size(20, 20, 25)
    min_position = Obstacle.Position(-40, 10, 0, 0)
    max_position = Obstacle.Position(30, 40, 0, 90)
    case_study_file="case_studies/mission1.yaml"
    generator = ObstacleGenerator(min_size, max_size, min_position, max_position, case_study_file=case_study_file)

    # Define a sample genotype
    genotype = [0, 0.05555556, 0.61111111, 0.6, 0.15714286, 0.36666667,
                0, 0.26666667, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0]

    # Call the genotype2phenotype method
    result = generator.genotype2phenotype(genotype)

    # Assert the expected output
    assert isinstance(result, TestCase)
    #assert result.test == "case_studies/mission1.yaml"
    assert len(result.test.simulation.obstacles) == 1
    assert isinstance(result.obstacles_list[0], Obstacle)
    assert result.obstacles_list[0].size.l == 2
    assert result.obstacles_list[0].size.w == 3
    assert result.obstacles_list[0].size.h == 4
    assert result.obstacles_list[0].position.x == 5
    assert result.obstacles_list[0].position.y == 6
    assert result.obstacles_list[0].position.z == 0
    assert result.obstacles_list[0].position.r == 8

# Run the test
test_genotype2phenotype()