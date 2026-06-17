export type AdminFieldType =
  | "text"
  | "textarea"
  | "number"
  | "date"
  | "url"
  | "checkbox"
  | "tags"
  | "json"
  | "select";

export interface AdminFieldConfig {
  name: string;
  label: string;
  type: AdminFieldType;
  required?: boolean;
  placeholder?: string;
  min?: number;
  max?: number;
  options?: string[];
  rows?: number;
}

export interface AdminContentRecord {
  id: number;
  [key: string]: unknown;
}

export interface AdminResourceConfig {
  key: string;
  label: string;
  singularLabel: string;
  endpoint: string;
  titleField: string;
  subtitleField?: string;
  fields: AdminFieldConfig[];
}