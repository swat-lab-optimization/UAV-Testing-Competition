import abc
import typing
import numpy as np
import typing 
import random
from shapely.geometry import Polygon
from ambiegen.generators.abstract_generator import AbstractGenerator
import yaml
#import cv2
import os
import logging #as log
log = logging.getLogger(__name__)
from aerialist.px4.obstacle import Obstacle
from aerialist.px4.drone_test import DroneTest
from testcase import TestCase
from shapely import geometry
from numpy import dot
from numpy.linalg import norm

class ObstacleGenerator(AbstractGenerator):
    """Abstract class for all generators."""

    def __init__(self, min_size:Obstacle, max_size:Obstacle, min_position:Obstacle, max_position:Obstacle, case_study_file: str, max_box_num:int=4):
        """Initialize the generator.

        Args:
            config (dict): Dictionary containing the configuration parameters.
        """
        super().__init__()
        self.min_size = min_size #[min_size.l, min_size.w, min_size.h]
        self.max_size = max_size #[max_size.l, max_size.w, max_size.h]
        self.min_position = min_position #[min_position.x, min_position.y, 0, min_position.r]
        self.max_position = max_position #[max_position.x, max_position.y, 0, max_position.r]
        self.case_study = DroneTest.from_yaml(case_study_file)
        self.max_box_num = max_box_num
        self.l_b, self.u_b = self.get_bounds()

    @property
    def size(self):
        return self.max_box_num*7 + 1
    

    def cmp_func(self, x, y):
        cos_sim = dot(x, y) / (norm(x) * norm(y))

        difference = 1 - abs(cos_sim)
        return difference
        

    def get_bounds(self):
        l_b = [1]
        u_b = [self.max_box_num]
        l_b_ = [self.min_size.l, self.min_size.w, self.min_size.h, self.min_position.x, self.min_position.y, 0, self.min_position.r]
        u_b_ = [self.max_size.l, self.max_size.w, self.max_size.h, self.max_position.x, self.max_position.y, 1, self.max_position.r]

        for i in range(self.max_box_num):
            l_b.append(l_b_)
            u_b.append(u_b_)


        l_b = self.flatten_test_case(l_b)
        u_b = self.flatten_test_case(u_b)

        return l_b, u_b
    
    def flatten_test_case(self, test):
        result = []
        for item in test:
            if isinstance(item, list):
                result.extend(self.flatten_test_case(item))
            else:
                result.append(item)
        return np.array(result)

    def generate_random_test(self, genotype=True):

        obstacles_list = []
        num_boxes = np.random.choice(np.arange(1, self.max_box_num+1))

        while len(obstacles_list) < (self.max_box_num):
            size = Obstacle.Size(
            l=random.choice(np.arange(self.min_size.l, self.max_size.l)),
            w=random.choice(np.arange(self.min_size.w, self.max_size.w)),
            h=random.choice(np.arange(self.min_size.h, self.max_size.h)),
            )
            position = Obstacle.Position(
            x=random.choice(np.arange(self.min_position.x, self.max_position.x)),
            y=random.choice(np.arange(self.min_position.y, self.max_position.y)),
            z=0,  # obstacles should always be place on the ground
            r=random.choice(np.arange(self.min_position.r, self.max_position.r)),
            )
            obstacle = Obstacle(size, position)

            to_include = self.obstacle_fits(obstacle, obstacles_list)
            if to_include:
                obstacles_list.append(obstacle)


        obstacles_list = obstacles_list[:num_boxes]

        #print("Genotype", self.genotype)
        the_test = TestCase(self.case_study, obstacles_list)

        self.genotype = self.phenotype2genotype(the_test)

        return the_test, True
    
    def normilize_flattened_test(self, test):
        result = (test - self.l_b)/(self.u_b - self.l_b)
        return result
    
    def denormilize_flattened_test(self, norm_test):
        result = norm_test*(self.u_b - self.l_b) + self.l_b
        return result
    
    def phenotype2genotype(self, phenotype):
        obstacles_list = phenotype.test.simulation.obstacles
        num_boxes = len(obstacles_list)
        tc = [num_boxes]
        for b in obstacles_list:
            tc.extend([b.size.l, b.size.w, b.size.h, b.position.x, b.position.y, 0, b.position.r])

        for r in range(num_boxes, self.max_box_num):
            tc.extend([self.min_size.l, self.min_size.w, self.min_size.h, self.min_position.x, self.min_position.y, 0, self.min_position.r])


        tc = self.normilize_flattened_test(tc)

        return tc

    def get_genotype(self):
        return self.genotype
    
    def get_phenotype(self):
        self.phenotype = self.genotype2phenotype(self.genotype)
        return self.phenotype
    

    def resize_test(self, test):
        num_boxes = int(round(test[0]))
        #print(f"num_boxes {num_boxes}")
        test = test[1:]
        # resize test to the shape (max_box_num, 7)
        test = test.reshape(-1, 7)

        return [num_boxes, test]
        
    def genotype2phenotype(self, genotype):

        denormilized_tc = self.denormilize_flattened_test(genotype)
        resized_tc = self.resize_test(denormilized_tc)
        num_boxes = resized_tc[0]
        tc = resized_tc[1]
        obstacles_list = []
        for b in range(num_boxes):
            size = Obstacle.Size(
            l=tc[b][0],
            w=tc[b][1],
            h=tc[b][2],
            )
            position = Obstacle.Position(
            x=tc[b][3],
            y=tc[b][4],
            z=0,  # obstacles should always be place on the ground
            r=tc[b][6],
            )
            obstacle = Obstacle(size, position)

            obstacles_list.append(obstacle)

        the_test = TestCase(self.case_study, obstacles_list)

        return the_test


    def obstacle_fits(self, obstacle:Obstacle, obstacles_list:list):

        new_box_geometry = obstacle.geometry#[obstacle.size.l, obstacle.size.w, obstacle.size.h]
        existing_boxes_geometry_list = [obstacle.geometry for obstacle in obstacles_list]#[obstacle.position.x, obstacle.position.y, obstacle.position.r]

        min_pos = [self.min_position.x, self.min_position.y]
        max_pos = [self.max_position.x, self.max_position.y]

        outer_polygon = geometry.Polygon([min_pos, [min_pos[0], max_pos[1]], max_pos, [max_pos[0], min_pos[1]]])
        

        for box in existing_boxes_geometry_list:
            if new_box_geometry.intersects(box):
                return False
        is_inside = new_box_geometry.within(outer_polygon)
        if not(is_inside):
            return False
        return True
    
    def visualize_test(self, test, save_dir:str ="./", save_path:str = "test.png"):
        test.plot()

    
        

        

        



        

        
        

