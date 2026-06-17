import {
  FilePenLine,
  ImagePlus,
  LoaderCircle,
  Pencil,
  Plus,
  RefreshCw,
  Search,
  Trash2,
} from "lucide-react";

import {
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";

import ContentEditorModal from "../../components/admin/ContentEditorModal";
import ProjectImageManager from "../../components/admin/ProjectImageManager";
import ResumeManager from "../../components/admin/ResumeManager";

import {
  useAdminAuth,
} from "../../contexts/AdminAuthContext";

import {
  publicApi,
} from "../../lib/api";

import {
  contentAdminApi,
} from "../../lib/contentAdminApi";

import {
  contentResources,
  profileResource,
} from "../../lib/contentResources";

import type {
  AdminContentRecord,
  AdminResourceConfig,
} from "../../types/contentAdmin";

import type {
  PortfolioData,
  Project,
} from "../../types/portfolio";

type SpecialTab =
  | "project-images"
  | "resumes";

type ActiveTab =
  | string
  | SpecialTab;

function recordTitle(
  resource: AdminResourceConfig,
  record: AdminContentRecord,
): string {
  const value =
    record[resource.titleField];

  return value === null ||
    value === undefined
    ? `${resource.singularLabel} #${record.id}`
    : String(value);
}

function recordSubtitle(
  resource: AdminResourceConfig,
  record: AdminContentRecord,
): string | null {
  if (!resource.subtitleField) {
    return null;
  }

  const value =
    record[resource.subtitleField];

  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return null;
  }

  return String(value);
}

function recordsForResource(
  data: PortfolioData,
  key: string,
): AdminContentRecord[] {
  if (key === "profile") {
    return [
      data.profile as unknown as AdminContentRecord,
    ];
  }

  const value =
    data[
      key as keyof PortfolioData
    ];

  if (!Array.isArray(value)) {
    return [];
  }

  return value as unknown as AdminContentRecord[];
}

export default function AdminContentPage() {
  const {
    token,
    logout,
  } = useAdminAuth();

  const [portfolio, setPortfolio] =
    useState<PortfolioData | null>(
      null,
    );

  const [activeTab, setActiveTab] =
    useState<ActiveTab>("profile");

  const [searchTerm, setSearchTerm] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const [editorResource, setEditorResource] =
    useState<AdminResourceConfig | null>(
      null,
    );

  const [editingRecord, setEditingRecord] =
    useState<AdminContentRecord | null>(
      null,
    );

  const [
    selectedProjectId,
    setSelectedProjectId,
  ] = useState<number | null>(null);

  const loadPortfolio = useCallback(
    async () => {
      setLoading(true);
      setError(null);

      try {
        const response =
          await publicApi.getPortfolio();

        setPortfolio(response);

        if (
          selectedProjectId === null &&
          response.projects.length > 0
        ) {
          setSelectedProjectId(
            response.projects[0].id,
          );
        }
      } catch (loadError) {
        setError(
          loadError instanceof Error
            ? loadError.message
            : "Could not load portfolio content.",
        );
      } finally {
        setLoading(false);
      }
    },
    [selectedProjectId],
  );

  useEffect(() => {
    void loadPortfolio();
  }, [loadPortfolio]);

  const activeResource = useMemo(() => {
    if (activeTab === "profile") {
      return profileResource;
    }

    return (
      contentResources.find(
        (resource) =>
          resource.key === activeTab,
      ) ?? null
    );
  }, [activeTab]);

  const displayedRecords = useMemo(() => {
    if (!portfolio || !activeResource) {
      return [];
    }

    const records =
      recordsForResource(
        portfolio,
        activeResource.key,
      );

    const normalizedSearch =
      searchTerm.trim().toLowerCase();

    if (!normalizedSearch) {
      return records;
    }

    return records.filter((record) => {
      const title = recordTitle(
        activeResource,
        record,
      ).toLowerCase();

      const subtitle =
        recordSubtitle(
          activeResource,
          record,
        )?.toLowerCase() ?? "";

      return (
        title.includes(
          normalizedSearch,
        ) ||
        subtitle.includes(
          normalizedSearch,
        )
      );
    });
  }, [
    activeResource,
    portfolio,
    searchTerm,
  ]);

  const selectedProject =
    portfolio?.projects.find(
      (project) =>
        project.id === selectedProjectId,
    ) ?? null;

  function openCreateEditor(
    resource: AdminResourceConfig,
  ) {
    setEditingRecord(null);
    setEditorResource(resource);
    setError(null);
  }

  function openEditEditor(
    resource: AdminResourceConfig,
    record: AdminContentRecord,
  ) {
    setEditingRecord(record);
    setEditorResource(resource);
    setError(null);
  }

  async function saveRecord(
    data: Record<string, unknown>,
  ) {
    if (!token || !editorResource) {
      return;
    }

    setSaving(true);
    setError(null);

    try {
      if (editingRecord) {
        await contentAdminApi.update(
          token,
          editorResource.endpoint,
          editingRecord.id,
          data,
        );
      } else {
        await contentAdminApi.create(
          token,
          editorResource.endpoint,
          data,
        );
      }

      setEditorResource(null);
      setEditingRecord(null);

      await loadPortfolio();
    } catch (saveError) {
      if (
        saveError instanceof Error &&
        saveError.message
          .toLowerCase()
          .includes("unauthorized")
      ) {
        logout();
        return;
      }

      setError(
        saveError instanceof Error
          ? saveError.message
          : "Could not save record.",
      );
    } finally {
      setSaving(false);
    }
  }

  async function deleteRecord(
    resource: AdminResourceConfig,
    record: AdminContentRecord,
  ) {
    if (
      !token ||
      !window.confirm(
        `Delete "${recordTitle(
          resource,
          record,
        )}"?`,
      )
    ) {
      return;
    }

    setError(null);

    try {
      await contentAdminApi.remove(
        token,
        resource.endpoint,
        record.id,
      );

      await loadPortfolio();
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Could not delete record.",
      );
    }
  }

  if (loading && !portfolio) {
    return (
      <div className="admin-page-state">
        <LoaderCircle
          className="spin"
          size={38}
        />

        <p>
          Loading portfolio content
        </p>
      </div>
    );
  }

  return (
    <section>
      <div className="admin-page-heading">
        <div>
          <span className="eyebrow">
            Portfolio Content
          </span>

          <h1>Content Manager</h1>

          <p>
            Create and update the public
            portfolio without editing source
            code.
          </p>
        </div>

        <button
          type="button"
          className="admin-icon-button"
          onClick={() => {
            void loadPortfolio();
          }}
          aria-label="Refresh content"
        >
          <RefreshCw size={19} />
        </button>
      </div>

      {error && (
        <div className="admin-alert admin-alert-error">
          {error}
        </div>
      )}

      <div className="content-manager-layout">
        <aside className="content-manager-sidebar">
          <button
            type="button"
            className={
              activeTab === "profile"
                ? "content-manager-tab content-manager-tab-active"
                : "content-manager-tab"
            }
            onClick={() => {
              setActiveTab("profile");
              setSearchTerm("");
            }}
          >
            <FilePenLine size={18} />
            Professional Profile
          </button>

          {contentResources.map(
            (resource) => (
              <button
                type="button"
                key={resource.key}
                className={
                  activeTab === resource.key
                    ? "content-manager-tab content-manager-tab-active"
                    : "content-manager-tab"
                }
                onClick={() => {
                  setActiveTab(
                    resource.key,
                  );
                  setSearchTerm("");
                }}
              >
                <FilePenLine
                  size={18}
                />
                {resource.label}
              </button>
            ),
          )}

          <button
            type="button"
            className={
              activeTab ===
              "project-images"
                ? "content-manager-tab content-manager-tab-active"
                : "content-manager-tab"
            }
            onClick={() => {
              setActiveTab(
                "project-images",
              );
              setSearchTerm("");
            }}
          >
            <ImagePlus size={18} />
            Project Screenshots
          </button>

          <button
            type="button"
            className={
              activeTab === "resumes"
                ? "content-manager-tab content-manager-tab-active"
                : "content-manager-tab"
            }
            onClick={() => {
              setActiveTab("resumes");
              setSearchTerm("");
            }}
          >
            <FilePenLine size={18} />
            Resumes
          </button>
        </aside>

        <div className="content-manager-main">
          {activeTab ===
          "project-images" ? (
            <>
              <div className="content-resource-toolbar">
                <div>
                  <h2>
                    Project Screenshots
                  </h2>

                  <p>
                    Choose a project and manage
                    its public images.
                  </p>
                </div>

                <select
                  value={
                    selectedProjectId ?? ""
                  }
                  onChange={(event) => {
                    setSelectedProjectId(
                      Number(
                        event.target.value,
                      ),
                    );
                  }}
                >
                  {portfolio?.projects.map(
                    (project) => (
                      <option
                        value={project.id}
                        key={project.id}
                      >
                        {project.title}
                      </option>
                    ),
                  )}
                </select>
              </div>

              {selectedProject ? (
                <ProjectImageManager
                  project={
                    selectedProject as Project
                  }
                  onChanged={
                    loadPortfolio
                  }
                />
              ) : (
                <div className="admin-empty-panel">
                  <ImagePlus size={36} />

                  <h2>
                    Create a project first
                  </h2>
                </div>
              )}
            </>
          ) : activeTab === "resumes" ? (
            <ResumeManager
              resumes={
                portfolio?.resumes ?? []
              }
              onChanged={loadPortfolio}
            />
          ) : activeResource ? (
            <>
              <div className="content-resource-toolbar">
                <div>
                  <h2>
                    {activeResource.label}
                  </h2>

                  <p>
                    Manage public portfolio
                    records.
                  </p>
                </div>

                <div className="content-resource-actions">
                  <label className="content-search">
                    <Search size={17} />

                    <input
                      value={searchTerm}
                      onChange={(event) => {
                        setSearchTerm(
                          event.target.value,
                        );
                      }}
                      placeholder="Search records"
                    />
                  </label>

                  {activeResource.key !==
                    "profile" && (
                    <button
                      type="button"
                      className="button button-primary"
                      onClick={() => {
                        openCreateEditor(
                          activeResource,
                        );
                      }}
                    >
                      <Plus size={18} />
                      Add{" "}
                      {
                        activeResource.singularLabel
                      }
                    </button>
                  )}
                </div>
              </div>

              {displayedRecords.length ===
              0 ? (
                <div className="admin-empty-panel">
                  <FilePenLine size={37} />

                  <h2>No records found</h2>

                  <p>
                    Add your first{" "}
                    {activeResource.singularLabel.toLowerCase()}.
                  </p>

                  <button
                    type="button"
                    className="button button-primary"
                    onClick={() => {
                      openCreateEditor(
                        activeResource,
                      );
                    }}
                  >
                    <Plus size={18} />
                    Add Record
                  </button>
                </div>
              ) : (
                <div className="content-record-list">
                  {displayedRecords.map(
                    (record) => {
                      const isVisible =
                        record.is_visible;

                      return (
                        <article
                          key={record.id}
                        >
                          <div className="content-record-order">
                            {String(
                              record.display_order ??
                                record.id,
                            )}
                          </div>

                          <div className="content-record-details">
                            <h3>
                              {recordTitle(
                                activeResource,
                                record,
                              )}
                            </h3>

                            {recordSubtitle(
                              activeResource,
                              record,
                            ) && (
                              <p>
                                {recordSubtitle(
                                  activeResource,
                                  record,
                                )}
                              </p>
                            )}

                            {typeof isVisible ===
                              "boolean" && (
                              <span
                                className={
                                  isVisible
                                    ? "content-visibility content-visible"
                                    : "content-visibility content-hidden"
                                }
                              >
                                {isVisible
                                  ? "Visible"
                                  : "Hidden"}
                              </span>
                            )}
                          </div>

                          <div className="content-record-actions">
                            <button
                              type="button"
                              onClick={() => {
                                openEditEditor(
                                  activeResource,
                                  record,
                                );
                              }}
                            >
                              <Pencil
                                size={17}
                              />
                              Edit
                            </button>

                            {activeResource.key !==
                              "profile" && (
                              <button
                                type="button"
                                className="content-delete-button"
                                onClick={() => {
                                  void deleteRecord(
                                    activeResource,
                                    record,
                                  );
                                }}
                              >
                                <Trash2
                                  size={17}
                                />
                                Delete
                              </button>
                            )}
                          </div>
                        </article>
                      );
                    },
                  )}
                </div>
              )}
            </>
          ) : null}
        </div>
      </div>

      {editorResource && (
        <ContentEditorModal
          resource={editorResource}
          record={editingRecord}
          saving={saving}
          error={error}
          onClose={() => {
            setEditorResource(null);
            setEditingRecord(null);
            setError(null);
          }}
          onSave={saveRecord}
        />
      )}
    </section>
  );
}