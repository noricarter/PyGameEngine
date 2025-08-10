from dataclasses import dataclass

@dataclass
class PhysicsBody:
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    mass: float = 1.0
    radius: float = 8.0