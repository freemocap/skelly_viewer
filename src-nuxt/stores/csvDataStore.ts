import { defineStore } from 'pinia';
import { invoke } from '@tauri-apps/api/tauri';
import type {ParseResult} from "papaparse";
import Papa from 'papaparse';

interface CsvDataState {
    headers: string[];
    rows: number[][];
}

export const useDataStore = defineStore('dataStore', {

    state: (): CsvDataState => ({
        headers: [],
        rows: [],
    }),

    actions: {
        async loadCSV(filePath: string) {
            try {
                // Read the file content using Tauri
                const fileContent: string = await invoke('read_file', { path: filePath });

                // Parse the CSV content
                Papa.parse<string[]>(fileContent, {
                    complete: (result: ParseResult<string[]>) => {
                        if (result.data.length > 0) {
                            this.headers = result.data[0] as string[];
                            this.rows = result.data.slice(1).map((row: string[]) =>
                                row.map((value: string) => parseFloat(value))
                            );
                        }
                    },
                    header: false,
                });
            } catch (error) {
                console.error('Error loading CSV file:', error);
            }
        }
    }
});
