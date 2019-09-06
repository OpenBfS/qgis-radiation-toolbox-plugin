<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" simplifyMaxScale="1" simplifyLocal="1" styleCategories="AllStyleCategories" maxScale="0" labelsEnabled="0" minScale="1e+08" version="3.6.2-Noosa" simplifyAlgorithm="0" readOnly="1" simplifyDrawingHints="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" enableorderby="0" forceraster="0" type="RuleRenderer">
    <rules key="{123e9b92-5bc2-4f15-984e-8c45d4c7fb27}">
      <rule filter="&quot;DHSR&quot; >= 0.000000 AND &quot;DHSR&quot; &lt;= 0.100000" symbol="0" label="&lt; 0.10" key="{618b54a9-b038-4b01-9f09-6478f08b283a}"/>
      <rule filter="&quot;DHSR&quot; > 0.100000 AND &quot;DHSR&quot; &lt;= 0.250000" symbol="1" label="0.10 - 0.25" key="{d11dc43e-7c45-47b7-a30a-e3e73addbe23}"/>
      <rule filter="&quot;DHSR&quot; > 0.250000 AND &quot;DHSR&quot; &lt;= 0.450000" symbol="2" label="0.25 - 0.45" key="{562576a2-94ce-468b-97c7-b40a4155f89a}"/>
      <rule filter="&quot;DHSR&quot; > 0.450000 AND &quot;DHSR&quot; &lt;= 1.000000" symbol="3" label="0.45 - 1.00" key="{b28a66b8-1067-4a60-bf11-7610864de7c0}"/>
      <rule filter="&quot;DHSR&quot; > 1.000000 AND &quot;DHSR&quot; &lt;= 5.000000" symbol="4" label="1.00 - 5.00" key="{9e4055a6-b02c-49f6-a5e7-6d1bb5ff3cd2}"/>
      <rule filter="&quot;DHSR&quot; > 5.000000 AND &quot;DHSR&quot; &lt;= 10.000000" symbol="5" label="5.00 - 10.00" key="{c0303ed4-36ad-40d6-8804-43e2b710c7e1}"/>
      <rule filter="ELSE" symbol="6" label=" > 10.00" key="{5a1a03ab-cd80-47c2-9eaf-ec056a10a7f8}"/>
    </rules>
    <symbols>
      <symbol alpha="1" force_rhr="0" name="0" type="marker" clip_to_extent="1">
        <layer class="SimpleMarker" pass="0" locked="0" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="26,150,65,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" force_rhr="0" name="1" type="marker" clip_to_extent="1">
        <layer class="SimpleMarker" pass="0" locked="0" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="166,217,106,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" force_rhr="0" name="2" type="marker" clip_to_extent="1">
        <layer class="SimpleMarker" pass="0" locked="0" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,255,20,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" force_rhr="0" name="3" type="marker" clip_to_extent="1">
        <layer class="SimpleMarker" pass="0" locked="0" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="253,141,60,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" force_rhr="0" name="4" type="marker" clip_to_extent="1">
        <layer class="SimpleMarker" pass="0" locked="0" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="240,59,32,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" force_rhr="0" name="5" type="marker" clip_to_extent="1">
        <layer class="SimpleMarker" pass="0" locked="0" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="164,0,35,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol alpha="1" force_rhr="0" name="6" type="marker" clip_to_extent="1">
        <layer class="SimpleMarker" pass="0" locked="0" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="96,0,1,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory minimumSize="0" rotationOffset="270" width="15" labelPlacementMethod="XHeight" minScaleDenominator="0" lineSizeType="MM" barWidth="5" backgroundColor="#ffffff" height="15" diagramOrientation="Up" sizeType="MM" opacity="1" sizeScale="3x:0,0,0,0,0,0" penColor="#000000" penAlpha="255" lineSizeScale="3x:0,0,0,0,0,0" maxScaleDenominator="1e+08" enabled="0" penWidth="0" scaleBasedVisibility="0" backgroundAlpha="255" scaleDependency="Area">
      <fontProperties style="tučné" description="Arial,14,-1,5,75,0,0,0,0,0,tučné"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" zIndex="0" dist="0" priority="0" obstacle="0" linePlacementFlags="18" placement="0">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="PA">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="CD">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="CT">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="CDT">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="PE">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="PN">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="PH">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AD_U-238">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AD_Th-232">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AA_Cs-137">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="DHSR">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="FID" field="fid"/>
    <alias index="1" name="point ID" field="PA"/>
    <alias index="2" name="date UTC" field="CD"/>
    <alias index="3" name="time UTC" field="CT"/>
    <alias index="4" name="datetime UTC" field="CDT"/>
    <alias index="5" name="PE (X longitude)" field="PE"/>
    <alias index="6" name="PN (Y latitude)" field="PN"/>
    <alias index="7" name="height m" field="PH"/>
    <alias index="8" name="" field=""/>
    <alias index="9" name="AD U-238 (AD Bq/kg)" field="AD_U-238"/>
    <alias index="10" name="AD Th-232 (AD Bq/kg)" field="AD_Th-232"/>
    <alias index="11" name="AA Cs-137 (AA Bq/m2)" field="AA_Cs-137"/>
    <alias index="12" name="DHSR μSv/h" field="DHSR"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="PA" applyOnUpdate="0"/>
    <default expression="" field="CD" applyOnUpdate="0"/>
    <default expression="" field="CT" applyOnUpdate="0"/>
    <default expression="" field="CDT" applyOnUpdate="0"/>
    <default expression="" field="PE" applyOnUpdate="0"/>
    <default expression="" field="PN" applyOnUpdate="0"/>
    <default expression="" field="PH" applyOnUpdate="0"/>
    <default expression="" field="" applyOnUpdate="0"/>
    <default expression="" field="AD_U-238" applyOnUpdate="0"/>
    <default expression="" field="AD_Th-232" applyOnUpdate="0"/>
    <default expression="" field="AA_Cs-137" applyOnUpdate="0"/>
    <default expression="" field="DHSR" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" exp_strength="0" constraints="3" unique_strength="1" field="fid"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="PA"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="CD"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="CT"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="CDT"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="PE"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="PN"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="PH"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field=""/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="AD_U-238"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="AD_Th-232"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="AA_Cs-137"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="DHSR"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="PA"/>
    <constraint exp="" desc="" field="CD"/>
    <constraint exp="" desc="" field="CT"/>
    <constraint exp="" desc="" field="CDT"/>
    <constraint exp="" desc="" field="PE"/>
    <constraint exp="" desc="" field="PN"/>
    <constraint exp="" desc="" field="PH"/>
    <constraint exp="" desc="" field=""/>
    <constraint exp="" desc="" field="AD_U-238"/>
    <constraint exp="" desc="" field="AD_Th-232"/>
    <constraint exp="" desc="" field="AA_Cs-137"/>
    <constraint exp="" desc="" field="DHSR"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column name="fid" width="-1" type="field" hidden="0"/>
      <column name="PA" width="-1" type="field" hidden="0"/>
      <column name="CD" width="-1" type="field" hidden="0"/>
      <column name="CT" width="-1" type="field" hidden="0"/>
      <column name="CDT" width="-1" type="field" hidden="0"/>
      <column name="PE" width="-1" type="field" hidden="0"/>
      <column name="PN" width="-1" type="field" hidden="0"/>
      <column name="PH" width="-1" type="field" hidden="0"/>
      <column name="" width="-1" type="field" hidden="0"/>
      <column name="AD_U-238" width="-1" type="field" hidden="0"/>
      <column name="AD_Th-232" width="-1" type="field" hidden="0"/>
      <column name="AA_Cs-137" width="-1" type="field" hidden="0"/>
      <column name="DHSR" width="-1" type="field" hidden="0"/>
      <column width="-1" type="actions" hidden="1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="" editable="1"/>
    <field name="AA_Cs-137" editable="1"/>
    <field name="AD_Th-232" editable="1"/>
    <field name="AD_U-238" editable="1"/>
    <field name="CD" editable="1"/>
    <field name="CDT" editable="1"/>
    <field name="CT" editable="1"/>
    <field name="DHSR" editable="1"/>
    <field name="PA" editable="1"/>
    <field name="PE" editable="1"/>
    <field name="PH" editable="1"/>
    <field name="PN" editable="1"/>
    <field name="fid" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="" labelOnTop="0"/>
    <field name="AA_Cs-137" labelOnTop="0"/>
    <field name="AD_Th-232" labelOnTop="0"/>
    <field name="AD_U-238" labelOnTop="0"/>
    <field name="CD" labelOnTop="0"/>
    <field name="CDT" labelOnTop="0"/>
    <field name="CT" labelOnTop="0"/>
    <field name="DHSR" labelOnTop="0"/>
    <field name="PA" labelOnTop="0"/>
    <field name="PE" labelOnTop="0"/>
    <field name="PH" labelOnTop="0"/>
    <field name="PN" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>fid</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
