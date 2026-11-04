# Helper: load the isolate table (Supplementary File 1) from the supplementary
# workbook and derive `Sample_type` from Supplementary File 3 (environmental
# sampling, which lists each environmental sample under its ward heading).
#
# Supplementary workbook layout: each sheet has a title in row 1 and the column
# headers in row 2, hence skip = 1.
#
# Sample_type values returned:
#   "Neonate, clinical" / "Other age group, clinical"
#   "Environmental, labour ward" / "Environmental, neonatal ward"
suppressPackageStartupMessages({library(readxl); library(dplyr); library(stringr); library(tidyr)})

load_supp_isolates <- function(path) {
  iso <- read_excel(path, sheet = "Supplementary_File1", skip = 1) %>%
    mutate(id = str_trim(as.character(id)))

  # If the workbook already carries a Sample_type column, use it as is.
  if ("Sample_type" %in% names(iso)) return(iso)

  # File 3: ward heading rows have text in column 1 and nothing in column 2
  env <- read_excel(path, sheet = "Supplementary_File3", skip = 1, col_names = FALSE,
                    .name_repair = "minimal")
  env <- env[, 1:2]; names(env) <- c("a", "lab_id")
  env <- env %>%
    mutate(a = as.character(a), lab_id = as.character(lab_id),
           ward = ifelse(is.na(lab_id) & str_detect(str_to_lower(a), "ward"), a, NA_character_)) %>%
    fill(ward) %>%
    filter(!is.na(lab_id), lab_id != "New_LabID") %>%
    transmute(id = str_trim(lab_id), ward = str_to_lower(str_trim(ward))) %>%
    distinct()

  # each sequenced environmental isolate must map to exactly one ward
  amb <- env %>% group_by(id) %>% filter(n_distinct(ward) > 1)
  if (nrow(amb) > 0) stop("Environmental isolate listed under more than one ward: ",
                          paste(unique(amb$id), collapse = ", "))
  env <- distinct(env, id, .keep_all = TRUE)

  iso %>%
    left_join(env, by = "id") %>%
    mutate(Sample_type = case_when(
      Status == "Environmental" & ward == "labour ward"   ~ "Environmental, labour ward",
      Status == "Environmental" & ward == "neonatal ward" ~ "Environmental, neonatal ward",
      Status == "Environmental"                           ~ "Environmental, unknown ward",
      Status == "Neonate"                                 ~ "Neonate, clinical",
      TRUE                                                ~ "Other age group, clinical")) %>%
    select(-ward)
}
