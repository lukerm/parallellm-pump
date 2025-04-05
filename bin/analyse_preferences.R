library("dplyr")
library("ggplot2")
library("hrbrthemes")
library("patchwork")
library("tidyr")

data_fname <- "~/parallellm-pump/data/responses/chatgpt_vs_claude_vs_deepseek_vs_gemini/llm_rank_data.csv"
df_rank <- read.csv(data_fname)

# Key grouping tables
df_group_overall <- df_rank %>%
    group_by(provider_responder) %>%
    summarize(mean_rank = mean(rank)) %>%
    arrange(mean_rank)

df_group_prompt <- df_rank %>%
    group_by(prompt_no, provider_responder) %>%
    summarize(mean_rank = mean(rank), mean_top1=mean(top1), mean_top2=mean(top2))

df_group_responder_rater <- df_rank %>%
  group_by(provider_responder, provider_rater) %>%
  summarize(rank = mean(rank, na.rm = TRUE), .groups = "drop") %>%
  rename(
    Responder = provider_responder,
    Rater = provider_rater
  )


# Boxplots

plot_top1 <- ggplot(df_group_prompt, aes(x=provider_responder, y=mean_top1, fill=provider_responder)) +
    geom_boxplot() +
    geom_dotplot(binaxis='y', stackdir='center', dotsize=0.4, fill="white") +
    labs(x="", y='Top-1 Rank (%)') +
    theme_ft_rc() +
    scale_fill_manual(values=c("#171717", "#D97757", "#4C6BFE", "#4698E4")) +
    ylim(c(-1, 100)) +
    theme(legend.position = "none", axis.title.y = element_text(size = 15))

plot_top2 <- ggplot(df_group_prompt, aes(x=provider_responder, y=mean_top2, fill=provider_responder)) +
    geom_boxplot() +
    geom_dotplot(binaxis='y', stackdir='center', dotsize=0.4, fill="white") +
    labs(x='LLM Provider', y='Top-2 Rank (%)') +
    theme_ft_rc() +
    scale_fill_manual(values=c("#171717", "#D97757", "#4C6BFE", "#4698E4")) +
    ylim(c(-1, 100)) +
    theme(legend.position = "none")


combined_plot <- (plot_top1 + plot_top2) +
  plot_layout(guides = "collect") &
  plot_annotation(title = "Comparison of Rankings by LLM Provider")

combined_plot & theme_ft_rc() &
  theme(
    plot.title = element_text(size = 20, hjust = 0.5),
    legend.position = "none",
    axis.title.x = element_text(size = 15),
    axis.title.y = element_text(size = 15),
  )


# Heatmap

ggplot(df_group_responder_rater, aes(x = Rater, y = Responder, fill = rank)) +
  geom_tile() +
  scale_fill_gradient2(low = "white", high = "red", midpoint=1) +
  theme_ft_rc() +
  labs(
    title = "Mean Rank by Responder and Rater",
    x = "Rater LLM",
    y = "Responder LLM",
    fill = "Mean Rank"
  ) +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    plot.title = element_text(hjust = 0.5),
    axis.title.x = element_text(size = 15),
    axis.title.y = element_text(size = 15),
  )
