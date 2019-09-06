<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" simplifyMaxScale="1" simplifyLocal="1" styleCategories="AllStyleCategories" maxScale="0" labelsEnabled="0" minScale="1e+08" version="3.6.2-Noosa" simplifyAlgorithm="0" readOnly="1" simplifyDrawingHints="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" enableorderby="0" forceraster="0" type="RuleRenderer">
    <rules key="{dd7da0a6-8665-4fb3-99ce-2099376edb8d}">
      <rule filter="&quot;FastDose&quot; >= 0.000000 AND &quot;FastDose&quot; &lt;= 0.150000" symbol="0" label="&lt; 0.15" key="{f6177060-f2e6-41b2-afb5-0f6e78011402}"/>
      <rule filter="&quot;FastDose&quot; > 0.150000 AND &quot;FastDose&quot; &lt;= 0.300000" symbol="1" label="0.15 - 0.30" key="{6cce3a69-be55-4148-9b93-9b1f0a477482}"/>
      <rule filter="&quot;FastDose&quot; > 0.300000 AND &quot;FastDose&quot; &lt;= 0.500000" symbol="2" label="0.30 - 0.50" key="{71004842-378c-4e08-803a-732378e5ce12}"/>
      <rule filter="&quot;FastDose&quot; > 0.500000 AND &quot;FastDose&quot; &lt;= 1.000000" symbol="3" label="0.50 - 1.00" key="{953d0d27-701a-47e5-85f2-0e7405085bee}"/>
      <rule filter="&quot;FastDose&quot; > 1.000000 AND &quot;FastDose&quot; &lt;= 5.000000" symbol="4" label="1.00 - 5.00" key="{fa831921-73ab-48a1-be61-ad2aa108009f}"/>
      <rule filter="&quot;FastDose&quot; > 5.000000 AND &quot;FastDose&quot; &lt;= 10.000000" symbol="5" label="5.00 - 10.00" key="{183dd99e-70f9-4101-b087-f5a062440014}"/>
      <rule filter="ELSE" symbol="6" label=" > 10.00" key="{ba016128-5d1f-4115-9ea9-ec38b576043f}"/>
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
          <prop k="outline_color" v="0,0,0,0"/>
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
          <prop k="outline_color" v="0,0,0,0"/>
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
          <prop k="outline_color" v="0,0,0,0"/>
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
          <prop k="outline_color" v="0,0,0,0"/>
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
          <prop k="outline_color" v="0,0,0,0"/>
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
          <prop k="outline_color" v="0,0,0,0"/>
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
    <field name="RECS">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AnrLat">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AnrLon">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AnrAlt">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AnrTime">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Lat">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Lon">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Gtm">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="GPSFix">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Stl">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Geos">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Galt">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Epoch">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Locked">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AccMark">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Station">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="TubeStatus">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RawSGgCt">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RawBGgCt">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="FastSGgCt">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="FltSGgCt">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="FastBGgCt">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="FltBGgCt">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="FastDose">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="FltDose">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Confid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="FID" field="fid"/>
    <alias index="1" name="RECS" field="RECS"/>
    <alias index="2" name="AnrLat" field="AnrLat"/>
    <alias index="3" name="AnrLon" field="AnrLon"/>
    <alias index="4" name="AnrAlt" field="AnrAlt"/>
    <alias index="5" name="AnrTime" field="AnrTime"/>
    <alias index="6" name="Lat" field="Lat"/>
    <alias index="7" name="Lon" field="Lon"/>
    <alias index="8" name="Gtm" field="Gtm"/>
    <alias index="9" name="GPSFix" field="GPSFix"/>
    <alias index="10" name="Stl" field="Stl"/>
    <alias index="11" name="Geos" field="Geos"/>
    <alias index="12" name="Galt" field="Galt"/>
    <alias index="13" name="Epoch" field="Epoch"/>
    <alias index="14" name="Locked" field="Locked"/>
    <alias index="15" name="AccMark" field="AccMark"/>
    <alias index="16" name="Station" field="Station"/>
    <alias index="17" name="TubeStatus" field="TubeStatus"/>
    <alias index="18" name="RawSGgCt" field="RawSGgCt"/>
    <alias index="19" name="RawBGgCt" field="RawBGgCt"/>
    <alias index="20" name="FastSGgCt" field="FastSGgCt"/>
    <alias index="21" name="FltSGgCt" field="FltSGgCt"/>
    <alias index="22" name="FastBGgCt" field="FastBGgCt"/>
    <alias index="23" name="FltBGgCt" field="FltBGgCt"/>
    <alias index="24" name="FastDose" field="FastDose"/>
    <alias index="25" name="FltDose" field="FltDose"/>
    <alias index="26" name="Confid" field="Confid"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="RECS" applyOnUpdate="0"/>
    <default expression="" field="AnrLat" applyOnUpdate="0"/>
    <default expression="" field="AnrLon" applyOnUpdate="0"/>
    <default expression="" field="AnrAlt" applyOnUpdate="0"/>
    <default expression="" field="AnrTime" applyOnUpdate="0"/>
    <default expression="" field="Lat" applyOnUpdate="0"/>
    <default expression="" field="Lon" applyOnUpdate="0"/>
    <default expression="" field="Gtm" applyOnUpdate="0"/>
    <default expression="" field="GPSFix" applyOnUpdate="0"/>
    <default expression="" field="Stl" applyOnUpdate="0"/>
    <default expression="" field="Geos" applyOnUpdate="0"/>
    <default expression="" field="Galt" applyOnUpdate="0"/>
    <default expression="" field="Epoch" applyOnUpdate="0"/>
    <default expression="" field="Locked" applyOnUpdate="0"/>
    <default expression="" field="AccMark" applyOnUpdate="0"/>
    <default expression="" field="Station" applyOnUpdate="0"/>
    <default expression="" field="TubeStatus" applyOnUpdate="0"/>
    <default expression="" field="RawSGgCt" applyOnUpdate="0"/>
    <default expression="" field="RawBGgCt" applyOnUpdate="0"/>
    <default expression="" field="FastSGgCt" applyOnUpdate="0"/>
    <default expression="" field="FltSGgCt" applyOnUpdate="0"/>
    <default expression="" field="FastBGgCt" applyOnUpdate="0"/>
    <default expression="" field="FltBGgCt" applyOnUpdate="0"/>
    <default expression="" field="FastDose" applyOnUpdate="0"/>
    <default expression="" field="FltDose" applyOnUpdate="0"/>
    <default expression="" field="Confid" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" exp_strength="0" constraints="3" unique_strength="1" field="fid"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="RECS"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="AnrLat"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="AnrLon"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="AnrAlt"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="AnrTime"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="Lat"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="Lon"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="Gtm"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="GPSFix"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="Stl"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="Geos"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="Galt"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="Epoch"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="Locked"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="AccMark"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="Station"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="TubeStatus"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="RawSGgCt"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="RawBGgCt"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="FastSGgCt"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="FltSGgCt"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="FastBGgCt"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="FltBGgCt"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="FastDose"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="FltDose"/>
    <constraint notnull_strength="0" exp_strength="0" constraints="0" unique_strength="0" field="Confid"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="RECS"/>
    <constraint exp="" desc="" field="AnrLat"/>
    <constraint exp="" desc="" field="AnrLon"/>
    <constraint exp="" desc="" field="AnrAlt"/>
    <constraint exp="" desc="" field="AnrTime"/>
    <constraint exp="" desc="" field="Lat"/>
    <constraint exp="" desc="" field="Lon"/>
    <constraint exp="" desc="" field="Gtm"/>
    <constraint exp="" desc="" field="GPSFix"/>
    <constraint exp="" desc="" field="Stl"/>
    <constraint exp="" desc="" field="Geos"/>
    <constraint exp="" desc="" field="Galt"/>
    <constraint exp="" desc="" field="Epoch"/>
    <constraint exp="" desc="" field="Locked"/>
    <constraint exp="" desc="" field="AccMark"/>
    <constraint exp="" desc="" field="Station"/>
    <constraint exp="" desc="" field="TubeStatus"/>
    <constraint exp="" desc="" field="RawSGgCt"/>
    <constraint exp="" desc="" field="RawBGgCt"/>
    <constraint exp="" desc="" field="FastSGgCt"/>
    <constraint exp="" desc="" field="FltSGgCt"/>
    <constraint exp="" desc="" field="FastBGgCt"/>
    <constraint exp="" desc="" field="FltBGgCt"/>
    <constraint exp="" desc="" field="FastDose"/>
    <constraint exp="" desc="" field="FltDose"/>
    <constraint exp="" desc="" field="Confid"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column name="fid" width="-1" type="field" hidden="0"/>
      <column name="RECS" width="-1" type="field" hidden="0"/>
      <column name="AnrLat" width="-1" type="field" hidden="0"/>
      <column name="AnrLon" width="-1" type="field" hidden="0"/>
      <column name="AnrAlt" width="-1" type="field" hidden="0"/>
      <column name="AnrTime" width="-1" type="field" hidden="0"/>
      <column name="Lat" width="-1" type="field" hidden="0"/>
      <column name="Lon" width="-1" type="field" hidden="0"/>
      <column name="Gtm" width="-1" type="field" hidden="0"/>
      <column name="GPSFix" width="-1" type="field" hidden="0"/>
      <column name="Stl" width="-1" type="field" hidden="0"/>
      <column name="Geos" width="-1" type="field" hidden="0"/>
      <column name="Galt" width="-1" type="field" hidden="0"/>
      <column name="Epoch" width="-1" type="field" hidden="0"/>
      <column name="Locked" width="-1" type="field" hidden="0"/>
      <column name="AccMark" width="-1" type="field" hidden="0"/>
      <column name="Station" width="-1" type="field" hidden="0"/>
      <column name="TubeStatus" width="-1" type="field" hidden="0"/>
      <column name="RawSGgCt" width="-1" type="field" hidden="0"/>
      <column name="RawBGgCt" width="-1" type="field" hidden="0"/>
      <column name="FastSGgCt" width="-1" type="field" hidden="0"/>
      <column name="FltSGgCt" width="-1" type="field" hidden="0"/>
      <column name="FastBGgCt" width="-1" type="field" hidden="0"/>
      <column name="FltBGgCt" width="-1" type="field" hidden="0"/>
      <column name="FastDose" width="-1" type="field" hidden="0"/>
      <column name="FltDose" width="-1" type="field" hidden="0"/>
      <column name="Confid" width="-1" type="field" hidden="0"/>
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
    <field name="AccMark" editable="1"/>
    <field name="AnrAlt" editable="1"/>
    <field name="AnrLat" editable="1"/>
    <field name="AnrLon" editable="1"/>
    <field name="AnrTime" editable="1"/>
    <field name="Confid" editable="1"/>
    <field name="Epoch" editable="1"/>
    <field name="FastBGgCt" editable="1"/>
    <field name="FastDose" editable="1"/>
    <field name="FastSGgCt" editable="1"/>
    <field name="FltBGgCt" editable="1"/>
    <field name="FltDose" editable="1"/>
    <field name="FltSGgCt" editable="1"/>
    <field name="GPSFix" editable="1"/>
    <field name="Galt" editable="1"/>
    <field name="Geos" editable="1"/>
    <field name="Gtm" editable="1"/>
    <field name="Lat" editable="1"/>
    <field name="Locked" editable="1"/>
    <field name="Lon" editable="1"/>
    <field name="RECS" editable="1"/>
    <field name="RawBGgCt" editable="1"/>
    <field name="RawSGgCt" editable="1"/>
    <field name="Station" editable="1"/>
    <field name="Stl" editable="1"/>
    <field name="TubeStatus" editable="1"/>
    <field name="fid" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="AccMark" labelOnTop="0"/>
    <field name="AnrAlt" labelOnTop="0"/>
    <field name="AnrLat" labelOnTop="0"/>
    <field name="AnrLon" labelOnTop="0"/>
    <field name="AnrTime" labelOnTop="0"/>
    <field name="Confid" labelOnTop="0"/>
    <field name="Epoch" labelOnTop="0"/>
    <field name="FastBGgCt" labelOnTop="0"/>
    <field name="FastDose" labelOnTop="0"/>
    <field name="FastSGgCt" labelOnTop="0"/>
    <field name="FltBGgCt" labelOnTop="0"/>
    <field name="FltDose" labelOnTop="0"/>
    <field name="FltSGgCt" labelOnTop="0"/>
    <field name="GPSFix" labelOnTop="0"/>
    <field name="Galt" labelOnTop="0"/>
    <field name="Geos" labelOnTop="0"/>
    <field name="Gtm" labelOnTop="0"/>
    <field name="Lat" labelOnTop="0"/>
    <field name="Locked" labelOnTop="0"/>
    <field name="Lon" labelOnTop="0"/>
    <field name="RECS" labelOnTop="0"/>
    <field name="RawBGgCt" labelOnTop="0"/>
    <field name="RawSGgCt" labelOnTop="0"/>
    <field name="Station" labelOnTop="0"/>
    <field name="Stl" labelOnTop="0"/>
    <field name="TubeStatus" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>fid</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
