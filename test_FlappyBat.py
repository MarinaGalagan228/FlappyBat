import unittest
import pygame
import FlappyBat
from FlappyBat import pipes, bat_rect, pipe, clouds, clouds_x


class TestGame(unittest.TestCase):
    def test_create_clouds(self):
        pygame.init()
        with self.assertRaises(TypeError):
            FlappyBat.create_clouds(clouds, None)
        with self.assertRaises(TypeError):
            FlappyBat.create_clouds('', clouds_x)

    def test_count_points(self):
        self.assertEqual(FlappyBat.count_points(pipes, 0), 2)
        self.assertEqual(FlappyBat.count_points(pipes, 2), 4)
        self.assertEqual(FlappyBat.count_points([], 0)[0], 'IndexError')
        self.assertIsNone(FlappyBat.count_points([], 0)[1])
        self.assertEqual(FlappyBat.count_points([400], None)[0], 'TypeError')
        self.assertIsNone(FlappyBat.count_points([400], None)[1])
        self.assertEqual(FlappyBat.count_points(None, None)[0], 'TypeError')
        self.assertIsNone(FlappyBat.count_points(None, None)[1])
        self.assertEqual(FlappyBat.count_points([None], 0)[0], 'AttributeError')
        self.assertIsNone(FlappyBat.count_points([None], 0)[1])

    def test_check_collision(self):
        pygame.init()
        pipes.extend(FlappyBat.create_pipe())
        if not FlappyBat.bat_rect.colliderect(pipe):
            self.assertFalse(FlappyBat.check_Collision(pipes, bat_rect))
        if FlappyBat.bat_rect.colliderect(pipe):
            self.assertTrue(FlappyBat.check_Collision(pipes, bat_rect))
        self.assertTrue(FlappyBat.check_Collision([400], 500))
        bat_rect.centery = list(range(0, 15)) + list(range(750, 780))
        self.assertFalse(FlappyBat.check_Collision([400], bat_rect))

    def test_move_pipes(self):
        pygame.init()
        self.assertIsNotNone(FlappyBat.move_pipes(pipes), pipes)
        self.assertEqual(FlappyBat.move_pipes(None)[0], 'TypeError')
        self.assertIsNone(FlappyBat.move_pipes(None)[1])
        self.assertEqual(FlappyBat.move_pipes([None])[0], 'AttributeError')
        self.assertIsNone(FlappyBat.move_pipes([None])[1])


if __name__ == '__main__':
    unittest.main()
