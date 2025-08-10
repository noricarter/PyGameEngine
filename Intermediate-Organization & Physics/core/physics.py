import math
from typing import Iterable, Protocol

class IPhysicsBody(Protocol):
    x: float; y: float
    vx: float; vy: float
    mass: float; radius: float

class Physics:
    """
    Newtonian gravity + simple collision resolution (stick-to-surface).
    - Gravity: a = G * m / r^2 toward each other body
    - Integration: semi-implicit Euler (v += a*dt, x += v*dt)
    - Collision: if overlapping, separate along the normal and
                 remove inward normal velocity (no bounce yet).
    """
    def __init__(self, G: float = 0.5):
        self.G = G

    def update(self, bodies: Iterable[IPhysicsBody], dt: float) -> None:
        bodies = list(bodies)

        # 1) Accumulate gravitational acceleration for each body
        ax_list = [0.0] * len(bodies)
        ay_list = [0.0] * len(bodies)

        for i, a in enumerate(bodies):
            if not hasattr(a, "mass"):  # skip non-physical
                continue
            ax = ay = 0.0
            for j, b in enumerate(bodies):
                if i == j or not hasattr(b, "mass"):
                    continue
                dx = b.x - a.x
                dy = b.y - a.y
                r2 = dx*dx + dy*dy
                if r2 == 0:
                    continue
                r = math.sqrt(r2)
                # avoid extreme forces inside overlap
                if r < getattr(a, "radius", 0) + getattr(b, "radius", 0):
                    continue
                a_mag = self.G * b.mass / r2
                ax += a_mag * dx / r
                ay += a_mag * dy / r
            ax_list[i] = ax
            ay_list[i] = ay

        # 2) Integrate velocities & positions
        for i, a in enumerate(bodies):
            if getattr(a, "static", False):  # <-- don't move static bodies
                continue
            if hasattr(a, "vx"):
                a.vx += ax_list[i] * dt
                a.vy += ay_list[i] * dt
                a.x += a.vx * dt
                a.y += a.vy * dt

        # 3) Resolve overlaps (project apart + kill inward normal speed)
        n = len(bodies)
        for i in range(n):
            a = bodies[i]
            if not hasattr(a, "radius"): continue
            for j in range(i+1, n):
                b = bodies[j]
                if not hasattr(b, "radius"): continue

                dx = b.x - a.x
                dy = b.y - a.y
                r2 = dx*dx + dy*dy
                if r2 == 0:
                    # on top of each other; nudge
                    dx, dy, r2 = 1e-6, 0.0, 1e-12
                dist = math.sqrt(r2)
                min_dist = a.radius + b.radius
                if dist >= min_dist:
                    continue

                # Normalized collision normal from a -> b
                nx = dx / dist
                ny = dy / dist
                overlap = min_dist - dist

                # Distribute separation (heavier moves less)
                ma = max(a.mass, 1e-6)
                mb = max(b.mass, 1e-6)
                total = ma + mb
                # If one body is much heavier (e.g., a planet), move the lighter almost entirely
                move_a = overlap * (mb / total)
                move_b = overlap * (ma / total)

                # Project out of overlap
                a.x -= nx * move_a
                a.y -= ny * move_a
                b.x += nx * move_b
                b.y += ny * move_b

                # Remove inward normal component of velocity (stick/no-bounce)
                # vn = v · n
                vna = a.vx * nx + a.vy * ny
                vnb = b.vx * nx + b.vy * ny

                # Only kill if moving toward each other along the normal
                rel_vn = vna - vnb
                if rel_vn > 0:  # a moving away from b along n -> ok
                    continue

                # Zero normal component (perfectly inelastic along the normal)
                a.vx -= vna * nx
                a.vy -= vna * ny
                b.vx -= vnb * nx
                b.vy -= vnb * ny
