import unittest
import pygame
import FlappyBat
from FlappyBat import pipes, bat_rect, pipe, clouds, clouds_x


class TestGame(unittest.TestCase):
    def test_create_clouds(self):
        pygame.init()
        screen = pygame.display.set_mode((580, 780))
        with self.assertRaises(AttributeError):
            FlappyBat.create_clouds(clouds, None)
        with self.assertRaises(TypeError):
            FlappyBat.create_clouds('', clouds_x)

    def test_check_collision(self):
        pygame.init()
        screen = pygame.display.set_mode((580, 780))
        pipes.extend(FlappyBat.create_pipe())
        self.assertTrue(FlappyBat.check_Collision(400, bat_rect))
        bat_rect.centery = list(range(0, 15)) + list(range(750, 780))
        self.assertFalse(FlappyBat.check_Collision(400, bat_rect))
        if not FlappyBat.bat_rect.colliderect(pipe):
            self.assertFalse(FlappyBat.check_Collision(400, bat_rect))
        if FlappyBat.bat_rect.colliderect(pipe):
            self.assertTrue(FlappyBat.check_Collision(400, bat_rect))

    def test_move_pipes(self):
        pygame.init()
        screen = pygame.display.set_mode((580, 780))
        self.assertIsNotNone(FlappyBat.move_pipes(pipes), pipes)
        self.assertEqual(FlappyBat.move_pipes([]), 'TypeError')
        self.assertIsNone(FlappyBat.move_pipes(None))


if __name__ == '__main__':
    unittest.main()
