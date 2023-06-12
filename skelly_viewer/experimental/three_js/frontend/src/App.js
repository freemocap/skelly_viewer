import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

function App() {
  const meshRef = useRef(null);

  useEffect(() => {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const animate = () => {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    }

    // Fetch the first frame from the FastAPI backend
    fetch(`http://localhost:8000/data/next_frame`)
      .then(response => response.json())
      .then(data => {
        // Create a Three.js object for each point in the data
        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });

        // Create meshes for the first frame and add them to the scene
        meshRef.current = Object.values(data.body).map(point => {
          const cube = new THREE.Mesh(geometry, material);
          cube.position.set(point.x, point.y, point.z);
          scene.add(cube);
          return cube;
        });

        // Start the animation loop
        animate();
      });

    // Set an interval to fetch the next frame and update the positions of the meshes
    setInterval(() => {
      fetch(`http://localhost:8000/data/next_frame`)
        .then(response => response.json())
        .then(data => {
          Object.values(data.body).forEach((point, i) => {
            meshRef.current[i].position.set(point.x, point.y, point.z);
          });
        });
    }, 1000 / 30);  // Update at 30 FPS
  }, []);

  return (
    <div className="App">
      {/* The canvas will be appended here by Three.js */}
    </div>
  );
}

export default App;
