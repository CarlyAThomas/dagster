import {ColorName} from './ColorName';

export const colorNameToVar: Record<ColorName, string> = {
  [ColorName.BrowserColorScheme]: 'var(--browser-color-scheme)',
  [ColorName.KeylineDefault]: 'var(--color-keyline-default)',
  [ColorName.LinkDefault]: 'var(--color-link-default)',
  [ColorName.LinkHover]: 'var(--color-link-hover)',
  [ColorName.LinkDisabled]: 'var(--color-link-disabled)',
  [ColorName.TextDefault]: 'var(--color-text-default)',
  [ColorName.TextLight]: 'var(--color-text-light)',
  [ColorName.TextLighter]: 'var(--color-text-lighter)',
  [ColorName.TextDisabled]: 'var(--color-text-disabled)',
  [ColorName.TextRed]: 'var(--color-text-red)',
  [ColorName.TextYellow]: 'var(--color-text-yellow)',
  [ColorName.TextGreen]: 'var(--color-text-green)',
  [ColorName.TextBlue]: 'var(--color-text-blue)',
  [ColorName.TextOlive]: 'var(--color-text-olive)',
  [ColorName.TextCyan]: 'var(--color-text-cyan)',
  [ColorName.TextLime]: 'var(--color-text-lime)',
  [ColorName.BackgroundDefault]: 'var(--color-background-default)',
  [ColorName.BackgroundDefaultHover]: 'var(--color-background-default-hover)',
  [ColorName.BackgroundLight]: 'var(--color-background-light)',
  [ColorName.BackgroundLightHover]: 'var(--color-background-light-hover)',
  [ColorName.BackgroundLighter]: 'var(--color-background-lighter)',
  [ColorName.BackgroundLighterHover]: 'var(--color-background-lighter-hover)',
  [ColorName.BackgroundDisabled]: 'var(--color-background-disabled)',
  [ColorName.BackgroundRed]: 'var(--color-background-red)',
  [ColorName.BackgroundRedHover]: 'var(--color-background-red-hover)',
  [ColorName.BackgroundYellow]: 'var(--color-background-yellow)',
  [ColorName.BackgroundYellowHover]: 'var(--color-background-yellow-hover)',
  [ColorName.BackgroundGreen]: 'var(--color-background-green)',
  [ColorName.BackgroundGreenHover]: 'var(--color-background-green-hover)',
  [ColorName.BackgroundBlue]: 'var(--color-background-blue)',
  [ColorName.BackgroundBlueHover]: 'var(--color-background-blue-hover)',
  [ColorName.BackgroundOlive]: 'var(--color-background-olive)',
  [ColorName.BackgroundOliverHover]: 'var(--color-background-oliver-hover)',
  [ColorName.BackgroundCyan]: 'var(--color-background-cyan)',
  [ColorName.BackgroundCyanHover]: 'var(--color-background-cyan-hover)',
  [ColorName.BackgroundLime]: 'var(--color-background-lime)',
  [ColorName.BackgroundLimeHover]: 'var(--color-background-lime-hover)',
  [ColorName.BackgroundGray]: 'var(--color-background-gray)',
  [ColorName.BackgroundGrayHover]: 'var(--color-background-gray-hover)',
  [ColorName.BorderDefault]: 'var(--color-border-default)',
  [ColorName.BorderHover]: 'var(--color-border-hover)',
  [ColorName.BorderDisabled]: 'var(--color-border-disabled)',
  [ColorName.FocusRing]: 'var(--color-focus-ring)',
  [ColorName.AccentPrimary]: 'var(--color-accent-primary)',
  [ColorName.AccentPrimaryHover]: 'var(--color-accent-primary-hover)',
  [ColorName.AccentReversed]: 'var(--color-accent-reversed)',
  [ColorName.AccentReversedHover]: 'var(--color-accent-reversed-hover)',
  [ColorName.AccentRed]: 'var(--color-accent-red)',
  [ColorName.AccentRedHover]: 'var(--color-accent-red-hover)',
  [ColorName.AccentYellow]: 'var(--color-accent-yellow)',
  [ColorName.AccentYellowHover]: 'var(--color-accent-yellow-hover)',
  [ColorName.AccentGreen]: 'var(--color-accent-green)',
  [ColorName.AccentGreenHover]: 'var(--color-accent-green-hover)',
  [ColorName.AccentBlue]: 'var(--color-accent-blue)',
  [ColorName.AccentBlueHover]: 'var(--color-accent-blue-hover)',
  [ColorName.AccentCyan]: 'var(--color-accent-cyan)',
  [ColorName.AccentCyanHover]: 'var(--color-accent-cyan-hover)',
  [ColorName.AccentLime]: 'var(--color-accent-lime)',
  [ColorName.AccentLimeHover]: 'var(--color-accent-lime-hover)',
  [ColorName.AccentLavender]: 'var(--color-accent-lavender)',
  [ColorName.AccentLavenderHover]: 'var(--color-accent-lavender-hover)',
  [ColorName.AccentOlive]: 'var(--color-accent-olive)',
  [ColorName.AccentOliveHover]: 'var(--color-accent-olive-hover)',
  [ColorName.AccentGray]: 'var(--color-accent-gray)',
  [ColorName.AccentGrayHover]: 'var(--color-accent-gray-hover)',
  [ColorName.AccentWhite]: 'var(--color-accent-white)',
  [ColorName.AlwaysWhite]: 'var(--color-always-white)',
  [ColorName.DialogBackground]: 'var(--color-dialog-background)',
  [ColorName.TooltipBackground]: 'var(--color-tooltip-background)',
  [ColorName.TooltipText]: 'var(--color-tooltip-text)',
  [ColorName.PopoverBackground]: 'var(--color-popover-background)',
  [ColorName.PopoverBackgroundHover]: 'var(--color-popover-background-hover)',
  [ColorName.ShadowDefault]: 'var(--color-shadow-default)',
  [ColorName.CheckboxUnchecked]: 'var(--color-checkbox-unchecked)',
  [ColorName.CheckboxChecked]: 'var(--color-checkbox-checked)',
  [ColorName.CheckboxDisabled]: 'var(--color-checkbox-disabled)',

  // Header
  [ColorName.NavBackground]: 'var(--color-nav-background)',
  [ColorName.NavText]: 'var(--color-nav-text)',
  [ColorName.NavTextHover]: 'var(--color-nav-text-hover)',
  [ColorName.NavTextSelected]: 'var(--color-nav-text-selected)',
  [ColorName.NavButton]: 'var(--color-nav-button)',
  [ColorName.NavButtonHover]: 'var(--color-nav-button-hover)',

  // Lineage Graph
  [ColorName.LineageEdge]: 'var(--color-lineage-edge)',
  [ColorName.LineageEdgeHighlighted]: 'var(--color-lineage-edge-highlighted)',
  [ColorName.LineageGroupNodeBackground]: 'var(--color-lineage-group-node-background)',
  [ColorName.LineageGroupNodeBackgroundHover]: 'var(--color-lineage-group-node-background-hover)',
  [ColorName.LineageGroupNodeBorder]: 'var(--color-lineage-group-node-border)',
  [ColorName.LineageGroupNodeBorderHover]: 'var(--color-lineage-group-node-border-hover)',
  [ColorName.LineageGroupBackground]: 'var(--color-lineage-group-background)',
  [ColorName.LineageNodeBackground]: 'var(--color-lineage-node-background)',
  [ColorName.LineageNodeBackgroundHover]: 'var(--color-lineage-node-background-hover)',
  [ColorName.LineageNodeBorder]: 'var(--color-lineage-node-border)',
  [ColorName.LineageNodeBorderHover]: 'var(--color-lineage-node-border-hover)',
  [ColorName.LineageNodeBorderSelected]: 'var(--color-lineage-node-border-selected)',

  // Dataviz
  [ColorName.DataVizBlue]: 'var(--color-data-viz-blue)',
  [ColorName.DataVizBlueAlt]: 'var(--color-data-viz-blue-alt)',
  [ColorName.DataVizBlurple]: 'var(--color-data-viz-blurple)',
  [ColorName.DataVizBlurpleAlt]: 'var(--color-data-viz-blurple-alt)',
  [ColorName.DataVizBrown]: 'var(--color-data-viz-brown)',
  [ColorName.DataVizBrownAlt]: 'var(--color-data-viz-brown-alt)',
  [ColorName.DataVizCyan]: 'var(--color-data-viz-cyan)',
  [ColorName.DataVizCyanAlt]: 'var(--color-data-viz-cyan-alt)',
  [ColorName.DataVizGray]: 'var(--color-data-viz-gray)',
  [ColorName.DataVizGrayAlt]: 'var(--color-data-viz-gray-alt)',
  [ColorName.DataVizGreen]: 'var(--color-data-viz-green)',
  [ColorName.DataVizGreenAlt]: 'var(--color-data-viz-green-alt)',
  [ColorName.DataVizLime]: 'var(--color-data-viz-lime)',
  [ColorName.DataVizLimeAlt]: 'var(--color-data-viz-lime-alt)',
  [ColorName.DataVizOrange]: 'var(--color-data-viz-orange)',
  [ColorName.DataVizOrangeAlt]: 'var(--color-data-viz-orange-alt)',
  [ColorName.DataVizPink]: 'var(--color-data-viz-pink)',
  [ColorName.DataVizPinkAlt]: 'var(--color-data-viz-pink-alt)',
  [ColorName.DataVizRed]: 'var(--color-data-viz-red)',
  [ColorName.DataVizRedAlt]: 'var(--color-data-viz-red-alt)',
  [ColorName.DataVizTeal]: 'var(--color-data-viz-teal)',
  [ColorName.DataVizTealAlt]: 'var(--color-data-viz-teal-alt)',
  [ColorName.DataVizViolet]: 'var(--color-data-viz-violet)',
  [ColorName.DataVizVioletAlt]: 'var(--color-data-viz-violet-alt)',
  [ColorName.DataVizYellow]: 'var(--color-data-viz-yellow)',
  [ColorName.DataVizYellowAlt]: 'var(--color-data-viz-yellow-alt)',

  //Gradients
  [ColorName.BlueGradient]: 'var(--color-blue-gradient)',
};
