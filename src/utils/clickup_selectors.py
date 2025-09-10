

class ClickUpSelectors:

    login_entry_selector = 'login-email-input'
    password_entry_selector = 'login-password-input'
    kanban_btn_selector = "//a[contains(., 'Kanban')]"
    grouping_btn_selector = '/html/body/app-root/cu-app-view-deferred/cu-app-view/cu-app-shell/cu-manager/div[1]/div/div/main/div/div/div/div/cu-dashboard/div/cu-views-bar-container/cu2-views-bar/div[2]/cu-views-settings-bar/div/div/cu-view-filter-controls/div/cu-view-grouping-dropdown/cu-view-grouping-settings/div/div/cu-view-setting-toggle/button'   # noqa: E501
    second_group_by_btn_selector = 'button.remove-button:nth-child(6)'   # noqa: E501
    kanban_selector = '.board-swimlane-view__list'
    delivered_column_selector = 'li.board-division__group-list-item:nth-child(6)'  # noqa: E501
    card_selector = './/li[contains(@class, "cdk-drag board-group__task-list-item")]'  # noqa: E501
    card_btn_selector = './/button[contains(@class, "open-task-clickable-area")]'  # noqa: E501
    name_html_element_selector = '/html/body/app-root/cu-app-view-deferred/cu-app-view/cu-task-keeper/cu-task-view/div/div/div[2]/cu-task-view-body/div/cu-task-view-task-content/div[1]/div[3]/cu-task-hero-section/cu-task-title/cu-slash-command/div/div[2]/h1'  # noqa: E501
    tag_html_element_selector = '/html/body/app-root/cu-app-view-deferred/cu-app-view/cu-task-keeper/cu-task-view/div/div/div[2]/cu-task-view-body/div/cu-task-view-task-content/div[1]/div[3]/cu-task-hero-section/div[3]/cu-task-fields-container/div/div[8]/div/cu-task-hero-section-tags-field/cu-task-hero-section-tags-dropdown/cu-tags-list/div/div/div/cu-tags-badge/div[1]/div/div/span'  # noqa: E501
    assignee_html_element_selector = '/html/body/app-root/cu-app-view-deferred/cu-app-view/cu-task-keeper/cu-task-view/div/div/div[2]/cu-task-view-body/div/cu-task-view-task-content/div[1]/div[3]/cu-task-hero-section/div[3]/cu-task-fields-container/div/div[2]/cu-assignees/cu-user-and-groups-list-dropdown/cu-user-list-dropdown/div/div/cu-user-group/cu-avatar-group/div/div[1]/div'  # noqa: E501
    task_details_btn_selector = '//*[@id="Comments"]'  # noqa: E501
    expand_task_history_btn_selector = '/html/body/app-root/cu-app-view-deferred/cu-app-view/cu-task-keeper/cu-task-view/div/div/div[2]/cu-task-view-body/div/cu-task-view-right-sidebar/div/cu-task-view-task-activity/cu-task-view-task-activity-lazy/div/cu-task-activity-stream/div/cu-task-activity-stream-item-wrapper[2]/div/div/button'  # noqa: E501
    task_history_html_element_selector = '/html/body/app-root/cu-app-view-deferred/cu-app-view/cu-task-keeper/cu-task-view/div/div/div[2]/cu-task-view-body/div/cu-task-view-right-sidebar/div/cu-task-view-task-activity/cu-task-view-task-activity-lazy/div/cu-task-activity-stream/div'  # noqa: E501
    card_config_menu_selector = '/html/body/app-root/cu-app-view-deferred/cu-app-view/cu-task-keeper/cu-task-view/div/div/cu-task-view-header/div[3]/cu-task-view-menu-dropdown-button/div/button'  # noqa: E501
    archive_card_btn_selector = "//button[contains(@data-pendo, 'user-settings-menu-item-cu-task-view-menu-archive')]"  # noqa: E501

    def list_name_btn_selector(list_name):
        return f"//span[text()='{list_name}']"
