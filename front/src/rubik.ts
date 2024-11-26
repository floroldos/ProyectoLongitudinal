import * as THREE from 'three';
import {cantSentinelas, movements, setSteps, solveMoves, stepList} from './scene'

export class Rubik {
    private readonly x: number;
    private readonly y: number;
    private readonly z: number;
    private readonly cube: THREE.Group;
    private centralMesh: THREE.Mesh;
    private readonly yOffset;
    private totalCubes = 0;
    private isAnimating = false;
    resolveMovements = 0;
    rotationTime;

    private currentIndex = 0;

    applyedMoves: string[] = [];
    applyedMovesCopy: string[] = [];

    goingBack = false;

    constructor(x: number = 3, y: number = 3, z: number = 3, speed: number = 200) {
        this.yOffset = y / 2;
        this.x = x;
        this.y = y;
        this.z = z;
        this.cube = new THREE.Group();
        this.centralMesh = new THREE.Mesh();
        this.createCube();
        this.createCentralMesh();
        this.cube.position.set(0, this.yOffset, 0);
        this.rotationTime = speed;
    }

    private createCube() {
        const colors = [
            '#ed3030', '#ff7b1c', 'white', '#f2f215', '#58d568', '#1c5ffe'
        ];

        const faceMaterials = colors.map(color => new THREE.MeshStandardMaterial({color}));

        for (let x = 0; x < this.x; x++) {
            for (let y = 0; y < this.y; y++) {
                for (let z = 0; z < this.z; z++) {
                    const geometry = new THREE.BoxGeometry(1, 1, 1);
                    const materials = faceMaterials.map(material => material.clone());
                    const mesh = new THREE.Mesh(geometry, materials);

                    mesh.position.set(
                        x - (this.x - 1) / 2,
                        y - (this.y - 1) / 2,
                        z - (this.z - 1) / 2
                    );
                    this.cube.add(mesh);
                    this.totalCubes++;

                    const edges = new THREE.EdgesGeometry(geometry);
                    const lineMaterial = new THREE.LineBasicMaterial({color: 'black', linewidth: 2});
                    const line = new THREE.LineSegments(edges, lineMaterial);
                    line.position.copy(mesh.position);
                    this.cube.add(line);
                    
                    
                }
            }
        }
    }
    
    arrows: Array<THREE.Group> = new Array<THREE.Group>();

    private createCentralMesh() {
        const geometry = new THREE.BoxGeometry(0, this.yOffset, 0);
        const material = new THREE.MeshStandardMaterial({ color: "gray" });
        this.centralMesh = new THREE.Mesh(geometry, material);
        this.centralMesh.position.set(0, this.yOffset, 0);
        this.cube.add(this.centralMesh);
    
        const cylinderRadius = 0.05;
        const cylinderHeight = 0.5;
        const cylinderColor = [
            "#a52c2c",
            "#cc5a10",
            "#b0b0b0",
            "#b4b40f",
            "#3ca03c",
            "#0e4abf"
        ];

        const rotations = [
            "R",
            "L",
            "U",
            "D",
            "F",
            "B"
        ]
    
        const createCylinder = (position: any, direction: any, color: any, rotation: any) => {
            const geometryBottom = new THREE.CylinderGeometry(cylinderRadius, cylinderRadius, cylinderHeight);
            const materialBottom = new THREE.MeshStandardMaterial({ color: color });
            const cylinderBottom = new THREE.Mesh(geometryBottom, materialBottom);

            const geometryTop = new THREE.CylinderGeometry(0 , cylinderRadius + 0.10, cylinderHeight);
            const materialTop = new THREE.MeshStandardMaterial({ color: color });
            const cylinderTop = new THREE.Mesh(geometryTop, materialTop);

            const group = new THREE.Group();

            cylinderBottom.position.copy(position);
            cylinderBottom.lookAt(position.clone().add(direction));
            cylinderBottom.rotateX(Math.PI / 2);

            cylinderTop.position.copy(position);
            cylinderTop.position.add(direction.clone().normalize().multiplyScalar(cylinderHeight));
            cylinderTop.lookAt(position.clone().add(direction));
            cylinderTop.rotateX(Math.PI / 2);

            group.add(cylinderBottom);
            group.add(cylinderTop);
            group.name = rotation;

            this.centralMesh.add(group);
            this.arrows.push(group);
        };

        createCylinder(
            this.centralMesh.position.clone().add(new THREE.Vector3(1.75, -2, 0)),
            new THREE.Vector3(1, 0, 0),
            cylinderColor[0],
            rotations[0]
        );

        createCylinder(
            this.centralMesh.position.clone().add(new THREE.Vector3(-1.75, -2, 0)),
            new THREE.Vector3(-1, 0, 0),
            cylinderColor[1],
            rotations[1]
        );

        createCylinder(
            this.centralMesh.position.clone().add(new THREE.Vector3(0, -0.25, 0)),
            new THREE.Vector3(0, 1, 0),
            cylinderColor[2],
            rotations[2]
        );

        createCylinder(
            this.centralMesh.position.clone().add(new THREE.Vector3(0, -3.75, 0)),
            new THREE.Vector3(0, -1, 0),
            cylinderColor[3],
            rotations[3]
        );

        createCylinder(
            this.centralMesh.position.clone().add(new THREE.Vector3(0, -2, 1.75)),
            new THREE.Vector3(0, 0, 1),
            cylinderColor[4],
            rotations[4]
        );

        createCylinder(
            this.centralMesh.position.clone().add(new THREE.Vector3(0, -2, -1.75)),
            new THREE.Vector3(0, 0, -1),
            cylinderColor[5],
            rotations[5]
        );
    }    

    public getX(): number {
        return this.x;
    }

    public getY(): number {
        return this.y;
    }

    public getZ(): number {
        return this.z;
    }

    public getCube(): THREE.Group {
        return this.cube;
    }

    public getCentralMesh(): THREE.Mesh {
        return this.centralMesh;
    }

    private rotateLayer(axis: 'x' | 'y' | 'z', layerPosition: number, angle: number) {
        const totalRotation = angle;

        if (this.isAnimating) return;
        this.isAnimating = true;

        let currentRotation = 0;
        const frames = Math.max(this.rotationTime / (1000 / 60));
        const rotationStep = angle / frames;

        if (layerPosition < 0) {
            layerPosition = layerPosition + (this.yOffset / this[`${axis}`]);
        } else {
            layerPosition = layerPosition - (this.yOffset / this[`${axis}`]);
        }

        const layer = this.cube.children.filter(child => {
            return child.position[axis] === layerPosition;
        });

        const tempGroup = new THREE.Group();
        layer.forEach(child => {
            this.cube.remove(child);
            tempGroup.add(child);
        });

        this.cube.add(tempGroup);

        const rotate = () => {
            if (Math.abs(currentRotation) < Math.abs(totalRotation)) {
                tempGroup.rotation[axis] += rotationStep;
                currentRotation += rotationStep;
                requestAnimationFrame(rotate);
            } else {
                tempGroup.rotation[axis] = totalRotation;

                while (tempGroup.children.length > 0) {
                    const child = tempGroup.children[0];
                    child.applyMatrix4(tempGroup.matrix);
                    tempGroup.remove(child);
                    this.cube.add(child);

                    child.position.x = Math.round(child.position.x * 1000000000000) / 1000000000000;
                    child.position.y = Math.round(child.position.y * 1000000000000) / 1000000000000;
                    child.position.z = Math.round(child.position.z * 1000000000000) / 1000000000000;
                }

                this.cube.remove(tempGroup);
                this.isAnimating = false;
            }
        };
        rotate();
    }

    public rotateU() {
        if (this.isAnimating) return;
        this.applyedMoves.push("U");
        this.generarBoton('U');
        this.rotateLayer('y', (this.y) / 2, -(Math.PI / 2));
    }

    public rotateUPrime() {
        if (this.isAnimating) return;
        this.applyedMoves.push("U'");
        this.generarBoton('U\'');
        this.rotateLayer('y', (this.y) / 2, (Math.PI / 2));
    }

    public rotateR() {
        if (this.isAnimating) return;
        this.applyedMoves.push("R");
        this.generarBoton('R');
        this.rotateLayer('x', (this.x) / 2, -(Math.PI / 2));
    }

    public rotateRPrime() {
        if (this.isAnimating) return;
        this.applyedMoves.push("R'");
        this.generarBoton('R\'');
        this.rotateLayer('x', (this.x) / 2, (Math.PI / 2));
    }

    public rotateF() {
        if (this.isAnimating) return;
        this.applyedMoves.push("F");
        this.generarBoton('F');
        this.rotateLayer('z', (this.z) / 2, -(Math.PI / 2));
    }

    public rotateFPrime() {
        if (this.isAnimating) return;
        this.applyedMoves.push("F'");
        this.generarBoton('F\'');
        this.rotateLayer('z', (this.z) / 2, (Math.PI / 2));
    }

    public rotateD() {
        if (this.isAnimating) return;
        this.applyedMoves.push("D");
        this.generarBoton('D');
        this.rotateLayer('y', -(this.y) / 2, (Math.PI / 2));
    }

    public rotateDPrime() {
        if (this.isAnimating) return;
        this.applyedMoves.push("D'");
        this.generarBoton('D\'');
        this.rotateLayer('y', -(this.y) / 2, -(Math.PI / 2));
    }

    public rotateL() {
        if (this.isAnimating) return;
        this.applyedMoves.push("L");
        this.generarBoton('L');
        this.rotateLayer('x', -(this.x) / 2, (Math.PI / 2));
    }

    public rotateLPrime() {
        if (this.isAnimating) return;
        this.applyedMoves.push("L'");
        this.generarBoton('L\'');
        this.rotateLayer('x', -(this.x) / 2, -(Math.PI / 2));
    }

    public rotateB() {
        if (this.isAnimating) return;
        this.applyedMoves.push("B");
        this.generarBoton('B');
        this.rotateLayer('z', -(this.z) / 2, (Math.PI / 2));
    }

    public rotateBPrime() {
        if (this.isAnimating) return;
        this.applyedMoves.push("B'");
        this.generarBoton('B\'');
        this.rotateLayer('z', -(this.z) / 2, -(Math.PI / 2));
    }

    lastSelected;

    public generarBoton(movimiento: string){
        if(this.goingBack) return;
        if (this.lastSelected)
        this.lastSelected.classList.remove('selected');
        const span = document.createElement('span'); 
        this.currentIndex += 1;
        span.id = this.currentIndex.toString();
        span.className = 'selected';
        this.lastSelected = span;
        span.onclick = () => {
            this.goToStep(parseInt(span.id));
        };
        span.textContent = movimiento;
        movements.insertBefore(span, movements.firstChild);
    }


    public goToStep(step: number){
        if (this.isAnimating) return;
        if (this.applyedMovesCopy.length > 0) {
            if (step == this.applyedMovesCopy.length + 1) return;
        }else{
            if (step == this.applyedMoves.length) return;
        }
        
        step = step - 1; // from 1 to 0 for list index

        if(!this.goingBack){
            this.applyedMovesCopy = JSON.parse(JSON.stringify(this.applyedMoves));
            this.goingBack = true;
        }

        let toApply = [];

        if (step < this.applyedMovesCopy.length){
            toApply = this.applyedMovesCopy.splice(step, this.applyedMovesCopy.length - step).reverse();
            this.lastSelected.classList.remove('selected');
            let span = document.getElementById((step + 1).toString());
            this.lastSelected = span;
            if (span){
                span.classList.add('selected');
            }
            for (let move of toApply){
                this.applyMoves(
                    move.length === 2 ? move[0] : move + "'"
                );
            }
        }else{
            toApply = JSON.parse(JSON.stringify(this.applyedMoves));
            // get the difference between the two arrays
            toApply = toApply.splice(this.applyedMovesCopy.length, step - this.applyedMovesCopy.length + 1);
            this.applyedMovesCopy = this.applyedMovesCopy.concat(toApply);

            this.lastSelected.classList.remove('selected');
            let span = document.getElementById((step + 1).toString());
            this.lastSelected = span;
            if (span){
                span.classList.add('selected');
            }
            for (let move of toApply){
                this.applyMoves(
                    move
                );
            }

        }
    }

    public shuffle() {

        const posiblesMoves = [
            'rotateU', 'rotateUPrime', 'rotateR', 'rotateRPrime',
            'rotateF', 'rotateFPrime', 'rotateD', 'rotateDPrime',
            'rotateL', 'rotateLPrime', 'rotateB', 'rotateBPrime'
        ];

        let tiempo = 0;
        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                const randomIndex = Math.floor(Math.random() * posiblesMoves.length);
                const randomMove = posiblesMoves[randomIndex];
                // @ts-ignore
                this[randomMove]();
            }, tiempo);
            tiempo += this.rotationTime;
        }
    }

    moveQueue: string[] = [];

    applyMoves(move: string) {
        console.log(move);
        if (move.length === 1) {
            this.moveQueue.push("rotate" + move);
        } else {
            if (move[0] === "|"){
                this.moveQueue.push(move);
            }else{
                this.moveQueue.push("rotate" + move[0] + "Prime");
            }
        }
        this.processQueue();
    }

    private processQueue() {
        if (this.isAnimating || this.moveQueue.length === 0) return;

        const move = this.moveQueue.shift();
         if (move[0] === "|"){
            const span = document.createElement('span');
            span.textContent = move.substring(1);
            span.className = 'hito';
            movements.insertBefore(span, movements.firstChild);
        }else {
            // @ts-ignore
            this[move]();
            this.resolveMovements++;
            solveMoves!.innerHTML = "- (" + this.resolveMovements + " / " + (stepList.length - cantSentinelas) + ")";
            if (this.resolveMovements === stepList.length) {
                solveMoves!.innerHTML = "- (" + stepList.length + " / " + (stepList.length - cantSentinelas) + ")";
            }
        }
        setTimeout(() => this.processQueue(), this.rotationTime);
    }

    reset(){
        this.moveQueue = [];
        movements.innerHTML = '';
        this.applyedMoves = [];
        setTimeout(() => {}, 250)
        {
            this.resetColors()
            this.shuffle();

            setTimeout(() => {
                const span = document.createElement('span');
                span.className = 'hito';
                span.textContent = 'Resolviendo...';
                movements.insertBefore(span, movements.firstChild);

                let moves = this.applyedMoves.join(",");
                console.log(this.applyedMoves)
                moves = moves + ",";
                moves = moves.substring(0, moves.length - 1);
                let url = "http://localhost:8000/resolve/" + moves;
                fetch(url, { method: "GET" })
                    .then((response) => response.json())
                    .then((json) => {
                        this.resolveMovements = 0;
                        solveMoves!.style.display = "none";
                        let steps = json.resolve;
                        steps = steps.endsWith(",")
                            ? steps.substring(0, steps.length - 1)
                            : steps;
                        setSteps(steps.split(","));
                        solveMoves!.style.display = "block";
                        solveMoves!.innerHTML = "(0 / " + (stepList.length - cantSentinelas) + ")";

                        stepList.forEach((step: string) => {
                            this.applyMoves(step);
                            if (step === "|Cubo resuelto"){
                                setTimeout(() => {
                                    this.reset();
                                }, this.moveQueue.length * this.rotationTime + 2500);
                            }
                        });
                    });
            }, 20 * this.rotationTime + 250)
        }
    }

    public resetColors() {
        const colors = [
            '#ed3030', '#ff7b1c', 'white', '#f2f215', '#58d568', '#1c5ffe'
        ];

        const faceMaterials = colors.map(color => new THREE.MeshStandardMaterial({ color }));

        // @ts-ignore
        this.cube.children.forEach((child, index) => {
            if (child instanceof THREE.Mesh) {
                const materials = faceMaterials.map(material => material.clone());
                child.material = materials;
            }
        });
    }
}
