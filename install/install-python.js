import { execa } from 'execa';
import * as fs from 'fs';
import os from 'os';
import * as path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);


let extension = '';
if (os.platform() === 'win32') {
    extension = '.exe';
}

async function main() {
    const scriptName = process.platform === 'win32' ? 'install-python.bat' : 'install-python.sh';
    const scriptPath = path.join(__dirname, scriptName);
    const pythonMainFileFullPath = path.join(__dirname, '../src-python/main.py')
    const pythonRequirementsFullPath = path.join(__dirname, '../install/requirements.txt')
    const binaryDestinationFolder = path.join(__dirname, '../dist')
    const tauriConfigPath =  path.join(__dirname, '../src-tauri/tauri.conf.json')

    console.log(`Load Tauri config from: ${tauriConfigPath}`)
    const data = fs.readFileSync(tauriConfigPath, 'utf8')
    const tauriConfig = JSON.parse(data);
    const binaryBaseName = tauriConfig.tauri.allowlist.shell.scope[0].name

    if (!fs.existsSync(scriptPath)) {
        console.error(`Script not found:${scriptPath}`);
        return;
    }

    if (!fs.existsSync(pythonMainFileFullPath)) {
        console.error(`Python main file not found: ${pythonMainFileFullPath}`);
        return;
    }

    const rustInfo = (await execa('rustc', ['-vV'])).stdout;
    const targetTriple = /host: (\S+)/g.exec(rustInfo)[1];
    if (!targetTriple) {
        console.error('Failed to determine platform target triple');
    } else {
        console.log(`Target triple (architecture, vender, operating system): ${targetTriple}`);
    }
    const targetBinaryName =`${binaryBaseName}-${targetTriple}${extension}`

    if (os.platform !== 'win32') {
        console.log('Setting script permissions to be executable...');
        await fs.promises.chmod(scriptPath, 0o755);
    }

    try {
        console.log(`Running the install script with args: \n'pythonRequirementsFullPath': ${pythonRequirementsFullPath}\n'targetBinaryName': ${targetBinaryName}, \n'pythonMainFilePath': ${pythonMainFileFullPath}\n'binaryDestinationFolder': ${binaryDestinationFolder}\n==================`);

        await execa(scriptPath, [pythonRequirementsFullPath, targetBinaryName, pythonMainFileFullPath, binaryDestinationFolder],{ stdio: 'inherit' });

        console.log(`=======================\n Script completed`)
    } catch (error) {
        console.error(`Failed to execute ${scriptName}:`, error);
        // Propagate the error to ensure the calling context is aware of the failure
        throw error;
    }
    console.log(`------------------------------------\nScript ${scriptName} execution complete - Check logs above for potential errors`);
}

main().catch((error) => {
    console.error('An error occurred:', error);
    process.exit(1);  // Ensure the process exits with an error status
});
