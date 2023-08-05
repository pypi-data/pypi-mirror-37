.. _iris.fileformats.rules:

======================
iris.fileformats.rules
======================



.. currentmodule:: iris

.. automodule:: iris.fileformats.rules

In this module:

 * :py:obj:`aux_factory`
 * :py:obj:`calculate_forecast_period`
 * :py:obj:`has_aux_factory`
 * :py:obj:`load_cubes`
 * :py:obj:`load_pairs_from_fields`
 * :py:obj:`log`
 * :py:obj:`scalar_cell_method`
 * :py:obj:`scalar_coord`
 * :py:obj:`vector_coord`
 * :py:obj:`CMAttribute`
 * :py:obj:`CMCustomAttribute`
 * :py:obj:`ConcreteReferenceTarget`
 * :py:obj:`ConversionMetadata`
 * :py:obj:`CoordAndDims`
 * :py:obj:`DebugString`
 * :py:obj:`Factory`
 * :py:obj:`FunctionRule`
 * :py:obj:`Loader`
 * :py:obj:`ProcedureRule`
 * :py:obj:`Reference`
 * :py:obj:`ReferenceTarget`
 * :py:obj:`Rule`
 * :py:obj:`RuleResult`
 * :py:obj:`RulesContainer`



.. autofunction:: iris.fileformats.rules.aux_factory


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


.. autofunction:: iris.fileformats.rules.calculate_forecast_period


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


.. autofunction:: iris.fileformats.rules.has_aux_factory


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


.. autofunction:: iris.fileformats.rules.load_cubes


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


.. autofunction:: iris.fileformats.rules.load_pairs_from_fields


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


.. autofunction:: iris.fileformats.rules.log


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


.. autofunction:: iris.fileformats.rules.scalar_cell_method


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


.. autofunction:: iris.fileformats.rules.scalar_coord


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


.. autofunction:: iris.fileformats.rules.vector_coord


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


Used by the rules for defining attributes on the Cube in a consistent manner.

.. deprecated:: 1.10

..

    .. autoclass:: iris.fileformats.rules.CMAttribute
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


Used by the rules for defining custom attributes on the Cube in a consistent manner.

.. deprecated:: 1.10

..

    .. autoclass:: iris.fileformats.rules.CMCustomAttribute
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


Everything you need to make a real Cube for a named reference.

..

    .. autoclass:: iris.fileformats.rules.ConcreteReferenceTarget
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


ConversionMetadata(factories, references, standard_name, long_name, units, attributes, cell_methods, dim_coords_and_dims, aux_coords_and_dims)

..

    .. autoclass:: iris.fileformats.rules.ConversionMetadata
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


Used within rules to represent a mapping of coordinate to data dimensions.

.. deprecated:: 1.10

..

    .. autoclass:: iris.fileformats.rules.CoordAndDims
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


Used by the rules for debug purposes

.. deprecated:: 1.10

..

    .. autoclass:: iris.fileformats.rules.DebugString
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


Factory(factory_class, args)

..

    .. autoclass:: iris.fileformats.rules.Factory
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


A Rule with values returned by its actions.

.. deprecated:: 1.10

..

    .. autoclass:: iris.fileformats.rules.FunctionRule
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


None

..

    .. autoclass:: iris.fileformats.rules.Loader
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


A Rule with nothing returned by its actions.

.. deprecated:: 1.10

..

    .. autoclass:: iris.fileformats.rules.ProcedureRule
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


None

..

    .. autoclass:: iris.fileformats.rules.Reference
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


ReferenceTarget(name, transform)

..

    .. autoclass:: iris.fileformats.rules.ReferenceTarget
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


A collection of condition expressions and their associated action expressions.

Example rule::

    IF
        f.lbuser[6] == 2
        f.lbuser[3] == 101
    THEN
        CMAttribute('standard_name', 'sea_water_potential_temperature')
        CMAttribute('units', 'Celsius')

.. deprecated:: 1.10

..

    .. autoclass:: iris.fileformats.rules.Rule
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


RuleResult(cube, matching_rules, factories)

..

    .. autoclass:: iris.fileformats.rules.RuleResult
        :members:
        :undoc-members:
        :inherited-members:


.. raw:: html

    <p class="hr_p"><a href="#">&uarr;&#32&#32 top &#32&#32&uarr;</a></p>
    <!--

-----------

.. raw:: html

    -->


A collection of :class:`Rule` instances, with the ability to read rule
definitions from files and run the rules against given fields.

.. deprecated:: 1.10

..

    .. autoclass:: iris.fileformats.rules.RulesContainer
        :members:
        :undoc-members:
        :inherited-members:

